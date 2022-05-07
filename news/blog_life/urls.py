from blog_life.views import TestView, Loadrun, Stoprun
from django.urls import path

urlpatterns = [
    path('', TestView.as_view(), name='blog_life'),
    path('load/', Loadrun.as_view(), name='loadlife'),
    path('stop/', Stoprun.as_view(), name='stoplife')
]
