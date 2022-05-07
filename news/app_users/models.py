from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    return f'profile_images/{instance.user.id}/{filename}'


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    profile_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True, default='profile_images/defaultuser.png', verbose_name=_('image'))
    profile_head_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True, default='profile_images/defaulthead.png', verbose_name=_('head image'))
    is_banned = models.BooleanField(null=True, default=False, verbose_name=_('banned'))
    news_count = models.IntegerField(default=0, verbose_name=_('news_count'))

    subscribers = models.ManyToManyField(User, related_name='subscribers', blank=True, verbose_name=_('subscribers'))
    subscriptions = models.ManyToManyField(User, related_name='subscriptions', blank=True, verbose_name=_('subscriptions'))

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')

    def __str__(self) -> str:
        """
        Возвращает имя пользователя (владельца профиля)
        :return: Имя пользователя
        :rtype: str
        """
        return self.user.username

    def increment_news_count(self):
        """
        Увеличивает количество новостей пользователя на 1"""
        self.news_count += 1
        self.save()

    def sub_count(self) -> int:
        """
        Возвращает количество подписчиков
        :return: количество подписчиков
        :rtype: int
        """
        return self.subscribers.all().count()

    def subs_count(self) -> int:
        """
        Возвращает количество подписок
        :return: количество подписок
        :rtype: int
        """
        return self.subscriptions.all().count()

