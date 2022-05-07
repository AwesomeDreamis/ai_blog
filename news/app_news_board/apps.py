from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppNewsBoardConfig(AppConfig):
    name = 'app_news_board'
    verbose_name = _('news')
