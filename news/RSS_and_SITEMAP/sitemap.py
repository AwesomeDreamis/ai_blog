from django.contrib.sitemaps import Sitemap
from app_news_board.models import News
from django.urls import reverse
from django.db.models import QuerySet


class NewsSitemap(Sitemap):
    """Карта новостей для карты сайта"""

    changefreq = 'daily'
    priority = 0.9

    def items(self) -> QuerySet:
        """
        Получение списка новостей
        :return: список новостей
        """
        return News.objects.all()

    def lastmod(self, obj: News):
        """
        Получение информации о последнем обновлении объекта
        :return: дата обновления
        """
        if obj.created_at == obj.updated_at:
            return obj.created_at
        else:
            return obj.updated_at


class StaticSitemap(Sitemap):
    """Карта статических страниц для карты сайта"""

    changefreq = 'weekly'
    priority = 0.9

    def items(self) -> list:
        """
        Получение списка статичных страниц для передачи в карту сайта
        :return: список названий (name в urls.py) представлений
        :rtype: list
        """
        return ['about', 'contacts']

    def location(self, item):
        return reverse(item)
