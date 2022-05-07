from django.urls import path
from .views import Login, Logout, RegisterView, ProfileView, ProfileUpdateView


urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:profile_id>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
