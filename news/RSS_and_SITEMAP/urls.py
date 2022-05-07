from django.urls import path, include
from RSS_and_SITEMAP.feeds import LatestNewsFeed


urlpatterns = [
    path('latest/feed/', LatestNewsFeed()),
]
