from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.urls import reverse
from app_news_board.models import News


class LatestNewsFeed(Feed):
    """Лента новостей"""

    title = "Новости"
    link = "/sitenews/"
    description = "Все новости"

    def items(self) -> QuerySet:
        return News.objects.order_by('-created_at')[:5]

    def item_title(self, item: News) -> str:
        return item.title

    def item_description(self, item: News) -> str:
        return item.content

    def item_link(self, item: News) -> str:
        return reverse('news_detail', args=[item.pk])
