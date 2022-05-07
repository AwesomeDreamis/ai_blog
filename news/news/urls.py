"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.sitemaps.views import sitemap
from RSS_and_SITEMAP.sitemap import NewsSitemap, StaticSitemap
# import debug_toolbar


schema_view = get_schema_view(
   openapi.Info(
      title="Library API",
      default_version='v1',
      description="online library",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@mail.ru"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)


sitemaps = {  # список составляющих карты сайта
    'static': StaticSitemap,
    'news': NewsSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_news_board.urls')),
    path('users/', include('app_users.urls')),
    path('blog/', include('app_blog.urls')),

    path('api/', include('API_data.urls')),

    path('rss/', include('RSS_and_SITEMAP.urls')),  # лента новостей
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),  # карта сайта
    path('i18n/', include('django.conf.urls.i18n')),  # интернационализация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),  # спецификации API и методов
    path('oauth', include('social_django.urls', namespace='social')),
    path('blog_life/', include('blog_life.urls')),  # приложение для симуляции жизни в блоге

    # path('__debug__/', include(debug_toolbar.urls))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
