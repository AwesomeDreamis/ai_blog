from django.urls import path
from API_data.views import UserAPI, UserDetailAPI, \
                            ProfileAPI, ProfileDetailAPI, \
                            PostAPI, PostDetailAPI, \
                            ImagesAPI, ImagesDetailAPI, \
                            CommentAPI, CommentDetailAPI

urlpatterns = [
    path('users/', UserAPI.as_view(), name='users_api_list'),
    path('users/<int:pk>/', UserDetailAPI.as_view(), name='users_api_detail'),

    path('profiles/', ProfileAPI.as_view(), name='profiles_api_list'),
    path('profiles/<int:pk>/', ProfileDetailAPI.as_view(), name='profiles_api_detail'),

    path('posts/', PostAPI.as_view(), name='posts_api_list'),
    path('posts/<int:pk>/', PostDetailAPI.as_view(), name='posts_api_detail'),

    path('images/', ImagesAPI.as_view(), name='images_api_list'),
    path('images/<int:pk>/', ImagesDetailAPI.as_view(), name='images_api_detail'),

    path('comments/', CommentAPI.as_view(), name='comments_api_list'),
    path('comments/<int:pk>/', CommentDetailAPI.as_view(), name='comments_api_detail'),

]
