from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    """Модель новости"""

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('author'))
    title = models.CharField(max_length=1500, db_index=True, default=None, blank=True, null=True, verbose_name=_('title'))  # используется только при симуляции жизни
    content = models.CharField(max_length=1500, default='', verbose_name=_('content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    views_count = models.IntegerField(default=0, verbose_name=_('views_count'))
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'))

    likes = models.ManyToManyField(User, related_name='likes', blank=True, verbose_name=_('likes'))
    saves = models.ManyToManyField(User, related_name='saves', blank=True, verbose_name=_('saves'))

    def get_absolute_url(self):
        """Метод для корректной работы карты сайта"""
        return reverse('news_detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = _('news')
        verbose_name = _('new')
        ordering = ['-id']

    def increment_view_count(self):
        """Увеличивает количество просмотрев новости на 1"""
        self.views_count += 1
        self.save()

    def total_likes(self):
        """Возвращает количество лайков"""
        return self.likes.all().count()


class Images(models.Model):
    """Модель изображений для новости"""

    news = models.ForeignKey(News, default=None, on_delete=models.CASCADE, verbose_name=_('news'))
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name=_('image'))

    class Meta:
        verbose_name_plural = _('images')
        verbose_name = _('image')


class Comment(models.Model):
    """Модель комментария"""

    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True, related_name='comment_news', verbose_name=_('new'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('user'))
    text = models.CharField(max_length=1500, default=None, null=True, verbose_name=_('text'))
    image = models.ImageField(upload_to='images/comment_images/', null=True, blank=True, verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    class Meta:
        verbose_name_plural = _('comments')
        verbose_name = _('comment')
