import os
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.http import HttpResponse, HttpResponseBadRequest
from app_news_board.models import News, Images, Comment
from app_news_board.forms import NewsForm, NewsImagesForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView
from django.db.models import F, Q, QuerySet
from datetime import datetime
from django.core.cache import cache


class NewsListView(ListView):
    """Представление новостей от всех пользователей"""

    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'all_news'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        # if self.request.user.groups.filter(name='moderators').exists():
        #     context['is_moderator'] = True
        return context

    def get_queryset(self) -> QuerySet:
        """
        Возвращает множество новостей всех пользователей
        :return: Множество новстей
        :rtype: QuerySet
        """
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            queryset = News.objects \
                .select_related('author__profile', ) \
                .prefetch_related('likes', 'saves') \
                .filter(content__icontains=query, is_active=True) \
                .order_by('-created_at')
        else:
            queryset = News.objects \
                .select_related('author__profile', ) \
                .prefetch_related('likes', 'saves') \
                .filter(is_active=True).order_by('-created_at') \
                .order_by('-created_at')
        return queryset


class NewsDetailView(DetailView, generic.edit.FormMixin):
    """Детальное представление новости"""
    model = News
    form_class = CommentForm
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        """Передаёт аргументы в шаблон"""
        context = super(NewsDetailView, self).get_context_data(**kwargs)

        post = get_object_or_404(News, id=self.kwargs['pk'])

        context['post'] = post

        if self.request.user.groups.filter(name='moderators').exists():
            context['is_moderator'] = True

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views_count = F('views_count') + 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        """Получает объект новости"""
        item = super().get_object(queryset)
        return item

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            self.object = self.get_object()
            form.save()
            return self.form_valid(form)
        else:
            self.object = self.get_object()
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('news_detail', kwargs={'pk': self.get_object().id})

    def form_valid(self, form):
        self.comment_object = form.save(commit=False)
        self.comment_object.news = self.get_object()
        if self.request.user.is_authenticated:
            self.comment_object.user = self.request.user
        self.comment_object.save()
        return super().form_valid(form)

#########################################################################################


class NewsCreateView(View):
    """Представление создания новости"""

    def get(self, request):
        is_moderator = False
        form = NewsForm
        images_form = NewsImagesForm

        if request.user.groups.filter(name='moderators').exists():
            is_moderator = True

        return render(request, 'news/create.html', {'form': form,
                                                    'images_form': images_form,
                                                    'is_moderator': is_moderator})

    def post(self, request):
        is_moderator = False
        user = request.user
        form = NewsForm(request.POST)
        images_form = NewsImagesForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')

        if form.is_valid() and images_form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.author = user
            news_instance.author.profile.increment_news_count()
            news_instance.save()
            for i in images:
                image_instance = Images(image=i, news=news_instance)
                image_instance.save()

            # здесь нужно фильтр по тексту, чтобы если не подобающий материал, то is_active=False

            return HttpResponseRedirect('/')
        else:
            if request.user.groups.filter(name='moderators').exists():
                is_moderator = True
            return render(request, 'news/create.html', {'form': form,
                                                    'images_form': images_form,
                                                    'is_moderator': is_moderator})


class NewsEditFormView(View):
    """Представление редактирования новости"""

    def get(self, request, profile_id):
        news = News.objects.get(id=profile_id)
        news_form = NewsForm(instance=news)

        is_moderator = False
        if request.user.groups.filter(name='moderators').exists():
            is_moderator = True

        if not request.user == news.author:
            if not request.user.groups.filter(name='moderators').exists():
                raise PermissionDenied()

        return render(request, 'news/edit.html', context={'news': news,
                                                          'news_form': news_form,
                                                          'profile_id': profile_id,
                                                          'is_moderator': is_moderator})

    def post(self, request, profile_id):
        news = News.objects.get(id=profile_id)
        news_form = NewsForm(request.POST, instance=news)
        author = news.author

        if news_form.is_valid():
            news_instance = news_form.save(commit=False)
            news_instance.author = author
            news_instance.updated_at = datetime.now()
            news_instance.save()
            return HttpResponseRedirect('/')
        return render(request, 'news/edit.html', context={'news': news, 'news_form': news_form, 'profile_id': profile_id})


class NewsDeleteView(DeleteView):
    """Представление удаления новости"""

    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')

    def get(self, request, *args, **kwargs):
        news = News.objects.get(id=super().get_object().id)

        if not request.user == news.author:
            if not request.user.groups.filter(name='moderators').exists():
                raise PermissionDenied()

        return render(request, 'news/delete.html')


# ========================================================================================


class NeedModeration(ListView):
    """Представление с отрепорченными новостями"""

    model = News
    template_name = 'news/need_moderation.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        posts = []
        queryset = []

        for post in News.objects.all():
            posts.append(post)

        for post in posts:
            if Comment.objects.filter(news__id=post.id).count() >= 1:
                queryset.append(post)

        return queryset


# ========================================================================================


class CommentDeleteView(DeleteView):
    """Представление удаления комментария"""

    model = Comment
    template_name = 'news/comment_delete.html'

    def get(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=super().get_object().id)

        if not request.user.groups.filter(name='moderators').exists():
            if not request.user == comment.user:
                raise PermissionDenied()
            raise PermissionDenied()

        return render(request, 'news/comment_delete.html')

    def get_success_url(self, **kwargs):
        return reverse_lazy('news_detail', kwargs={'pk': self.get_object().news.id})


# ========================================================================================


class LikePost(View):
    """Лайк новости"""

    def post(self, request):
        user = request.user
        post_id = request.POST.get('post_id')
        post_obj = News.objects.get(id=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        return redirect('news_list')


class SavePost(View):
    """Сохранение новости"""
    def post(self, request):
        user = request.user
        post_id = request.POST.get('post_id')
        post_obj = News.objects.get(id=post_id)

        if user in post_obj.saves.all():
            post_obj.saves.remove(user)
        else:
            post_obj.saves.add(user)

        return redirect('news_list')


# ========================================================================================


class Contacts(View):
    """Представление с контактами"""
    def get(self, request):
        return render(request, 'static/contacts.html')


class About(View):
    """Представление с информацией о компании"""
    def get(self, request):
        return render(request, 'static/about.html')


# ========================================================================================


def get_news_in_custom_format(request):
    """
    Возвращает список новостей в указанном формате
    :param request:
    :return: data
    """

    format = request.GET['format']
    if format not in ['xml', 'json', 'yaml']:
        return HttpResponseBadRequest()
    data = serializers.serialize(format, News.objects.all())
    return HttpResponse(data)
