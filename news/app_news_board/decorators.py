from functools import wraps
from django.db.models import F
from django.db import transaction
from app_news_board.models import News


def counted(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            counter, created = News.objects.get_or_create(url=request.path)
            counter.views_count = F('views_count') + 1
            counter.save()
        return f(request, *args, **kwargs)
    return decorator
