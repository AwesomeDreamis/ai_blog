import os

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views import View
from django.contrib.auth.models import User
from app_users.models import Profile
from app_news_board.models import News, Comment, Images
import random
import subprocess
import signal
import logging
import psutil
from psutil import NoSuchProcess
import requests
import json

logger = logging.getLogger(__name__)


class TestView(View):
    """Представление с настройками жизни"""

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='moderators').exists():
            raise PermissionDenied()

        context = {
            'users': User.objects.all(),
            'rand_user': random.choice(User.objects.all()),
            'news': News.objects.all(),
            'comments': Comment.objects.all(),
        }

        return render(request, 'blog_life/blog_life.html', context=context)


processes = []
info = {
    'users': 0,
    'posts': 0,
    'comments': 0,
}


class Loadrun(View):
    """Представление (кнопка) запускающая процесс в директории 'management'."""

    def post(self, request):
        """Функция запускающая процесс и передаёт в него следующие параметры:
        - секунды между действиями
        - выполняется ли действие (
                                - регистрация,
                                - добавление поста,
                                - добавление комментария,
                                - лайк или сохранение,
                                - подписка
                                )
        - вероятность выполнения каждого действия
        """

        info['users'] = User.objects.all().count()
        info['posts'] = News.objects.all().count()
        info['comments'] = Comment.objects.all().count()

        seconds = request.POST.get('seconds')
        parameters = request.POST.getlist('parameters')
        parameters_values = request.POST.getlist('parameters_value')

        if len(parameters) == 0:
            print('не выбрано ни одного параметра')
            'You need choose at least one parameter'
            return redirect('blog_life')
        else:
            param_dict = {'user': [0, 0],
                          'post': [0, 0],
                          'comment': [0, 0],
                          'like_save': [0, 0],
                          'sub': [0, 0]}

            for num, i in enumerate(param_dict):
                if i in parameters:
                    param_dict[i][0] = 1
                    param_dict[i][1] = parameters_values[num]

            if len(processes) >= 1:  # если в списке уже есть процесс, то новый процесс запущен не будет
                pass
            else:  # если в списке нет процессов, то запускается процесс и его PID добавляется в список
                simulate_life = subprocess.Popen([
                    "env\Scripts\\python", "manage.py", "loadlife",
                    f"{seconds}",  # saturation of life

                    f"{param_dict['user'][0]}",  # is the user enabled
                    f"{param_dict['post'][0]}",  # is the post enabled
                    f"{param_dict['comment'][0]}",  # is the comment enabled
                    f"{param_dict['like_save'][0]}",  # is the like/save enabled
                    f"{param_dict['sub'][0]}",  # is the sub enabled

                    f"{param_dict['user'][1]}",  # user weight
                    f"{param_dict['post'][1]}",  # post weight
                    f"{param_dict['comment'][1]}",  # comment weight
                    f"{param_dict['like_save'][1]}",  # like/save weight
                    f"{param_dict['sub'][1]}"  # sub weight
                ])

                pid = simulate_life.pid
                processes.append(pid)
                logger.info(f"Запущена симуляция жизни в блоге")
                logger.info(f"process pid {pid}")
                logger.info(f"process pid {processes}")

            return redirect('blog_life')


class Stoprun(View):
    """Останавливает процесс симуляции"""

    def post(self, request):
        """Завершает процесс по PID, находящемуся в списке 'processes' """
        # try:
        if len(processes) == 0:
            logger.info(f"нет запущенных процессов")
            return redirect('blog_life')
        else:
            logger.info(f"Завершён процесс симуляции жизни {processes[0]}")
            for pid in processes:
                proc = psutil.Process(pid)
                proc.terminate()
                processes.remove(pid)

            created_users = User.objects.all().count() - info['users']
            created_posts = News.objects.all().count() - info['posts']
            created_comments = Comment.objects.all().count() - info['comments']

            info['users'] = created_users
            info['posts'] = created_posts
            info['comments'] = created_comments

            print('процесс завершён')
            logger.info(f"process pid {processes}")
            logger.info(f"Создано пользователей: {created_users}\n"
                        f"Создано новостей: {created_posts}\n"
                        f"Создано комментариев: {created_comments}")

            return redirect('blog_life')
        # except NoSuchProcess:
        #     return redirect('blog_life')
