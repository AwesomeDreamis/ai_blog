import json
import requests
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from app_news_board.models import News
from app_blog.forms import UploadPostForm
from django.views.generic import ListView
from django.core.paginator import Paginator


class BlogView(View):
    """Представление блога"""

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        profile_data = user.profile
        all_posts = News.objects \
            .select_related('author__profile', ) \
            .prefetch_related('likes', 'saves') \
            .filter(author=user)\
            .order_by('-created_at')
        paginator = Paginator(all_posts, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/blog.html', context={'user': user,
                                                          'profile': profile_data,
                                                          'profile_id': pk,
                                                          'all_posts': page_obj, })


class BookmarksView(ListView):
    """Представление сохранённых постов"""

    model = News
    template_name = 'blog/bookmarks.html'
    context_object_name = 'saved_posts'
    paginate_by = 20

    def get_queryset(self):
        """
        Возвращает множество постов, которые сохранил пользователь
        :return: множество постов сохранённых пользователем
        :rtype: Queryset
        """

        user = self.request.user
        queryset = News.objects \
            .select_related('author__profile', ) \
            .prefetch_related('likes', 'saves') \
            .filter(saves=user).reverse()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Возвращает данные, передаваемые в шаблон"""
        context = super(BookmarksView, self).get_context_data(**kwargs)

        context['user'] = self.request.user

        return context


class SubscriptionsView(ListView):
    """Представление основной страницы, отображающей посты, сделанные пользователями на которых вы подписаны"""

    model = News
    template_name = 'blog/subscriptions.html'
    context_object_name = 'sub_posts'
    paginate_by = 20

    def get_queryset(self):
        """
        Возвращает множество постов от ваших подписок
        :return: множество постов от ваших подписок
        :rtype: Queryset
        """

        user = self.request.user
        if user.profile.subs_count() > 0:
            queryset = News.objects \
                .select_related('author__profile', ) \
                .prefetch_related('likes', 'saves') \
                .filter(author__in=user.profile.subscriptions.all()) \
                .order_by('-created_at')
        else:
            queryset = []
        return queryset


class SubscriptionsList(View):
    """Представление со списком подписок пользователя"""

    def get(self, request):
        if self.request.GET.get('search'):
            query = self.request.GET.get('search')
            queryset = request.user.profile.subscriptions.filter(username__icontains=query)
        else:
            queryset = request.user.profile.subscriptions.all()

        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/subscriptions_list.html', context={'data': page_obj})


class SubscribersList(View):
    """Представление со списком подписчиков пользователя"""

    def get(self, request, pk):
        user = User.objects.get(id=pk)

        if self.request.GET.get('search'):
            query = self.request.GET.get('search')
            queryset = user.profile.subscribers.filter(username__icontains=query)
        else:
            queryset = user.profile.subscribers.all()

        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/subscribers_list.html', context={'user': user, 'data': page_obj})


class Subscribe(View):
    """Подписаться/отписаться"""

    def post(self, request):
        user = request.user
        user_id = request.POST.get('user_id')
        user_obj = User.objects.get(id=user_id)

        if user in user_obj.profile.subscribers.all():
            user_obj.profile.subscribers.remove(user)
            user.profile.subscriptions.remove(user_obj)
        else:
            user_obj.profile.subscribers.add(user)
            user.profile.subscriptions.add(user_obj)

        user_obj.profile.save()
        user.profile.save()

        return redirect('subscriptions')


import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from django.conf import settings


class GetYoutubeData(View):

    def get(self, request):

        if self.request.GET.get('youtube_channel'):
            query = self.request.GET.get('youtube_channel')
            data = self.get_youtube_videos(query)
        else:
            data = []

        return render(request, 'functions/get_youtube_data.html', context={'data': data})

    def get_youtube_videos(self, query):
        api_key = settings.GOOGLE_DEVELOPER_KEY
        api_service_name = "youtube"
        api_version = "v3"
        youtube = googleapiclient.discovery.build(
            api_service_name,
            api_version,
            developerKey=api_key)

        response = youtube.search().list(
            part="snippet",
            q=f"{query}",
            maxResults=50
        ).execute()

        items = response.get("items")

        videos_data = {}
        for video in items:
            channel_id = video['snippet']['channelId']
            channel_info = self.get_chanel_data(youtube, channel_id)
            if 'videoId' in video['id'].keys() and \
                    int(channel_info['viewCount']) > 150000000 and \
                    int(channel_info['subscriberCount']) > 500000:
                videos_data[video['id']['videoId']] = video['snippet']['title']
        return videos_data

    def get_chanel_data(self, youtube, channel_id):

        request = youtube.channels().list(
            part="statistics",
            id=f"{channel_id}"
        )
        response = request.execute()
        info = dict(response)
        return info['items'][0]['statistics']

# def add_posts(request):
#     if request.method == 'POST':
#         upload_file_form = UploadPostForm(request.POST, request.FILES)
#         if upload_file_form.is_valid():
#             post_file = upload_file_form.cleaned_data['file'].read()
#             post_str = post_file.decode('utf-8-sig').split('\n')
#             csv_reader = reader(post_str, delimiter=";")
#             for row in csv_reader:
#                 if len(row) == 2:
#                     News.objects.create(title=None, author=request.user, content=row[0], created_at=row[1], is_active=False)
#             return HttpResponseRedirect('/')
#     else:
#         upload_file_form = UploadPostForm()
#
#     context = {'form': upload_file_form}
#     return render(request, 'blog/upload_file.html', context=context)

