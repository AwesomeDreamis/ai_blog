from django.urls import path
from .views import BlogView, BookmarksView, SubscriptionsView, SubscribersList, SubscriptionsList, Subscribe, GetYoutubeData

urlpatterns = [
    path('<int:pk>/', BlogView.as_view(), name='user_blog'),
    path('bookmarks/', BookmarksView.as_view(), name='bookmarks'),

    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('subscriptions_list/', SubscriptionsList.as_view(), name='subscriptions_list'),
    path('subscribers_list/<int:pk>/', SubscribersList.as_view(), name='subscribers_list'),

    path('subscribe/', Subscribe.as_view(), name='subscribe'),

    path('youtube_api/', GetYoutubeData.as_view(), name='youtube_data'),
]
