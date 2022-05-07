from django.urls import path
from .views import NewsListView, NewsDetailView, NewsEditFormView, NewsCreateView, NewsDeleteView, \
    get_news_in_custom_format, \
    CommentDeleteView, \
    LikePost, SavePost, \
    Contacts, About, \
    NeedModeration

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='create'),
    path('<int:profile_id>/edit/', NewsEditFormView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/comment_delete/', CommentDeleteView.as_view(), name='comment_delete'),

    path('need_moderation/', NeedModeration.as_view(), name='need_moderation'),

    path('like/', LikePost.as_view(), name='like_list'),
    path('save/', SavePost.as_view(), name='save_list'),

    path('contacts/', Contacts.as_view(), name='contacts'),
    path('about/', About.as_view(), name='about'),

    path('custom_news/', get_news_in_custom_format),

]
