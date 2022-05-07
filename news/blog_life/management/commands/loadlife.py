import json
import os
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
import time
from app_news_board.models import News, Comment, Images
from django.contrib.auth.models import User
from app_users.models import Profile
import random
import logging
from django.utils.crypto import get_random_string
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from django.conf import settings


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Кастомная команда
    'python manage.py loadlife <seconds> <user_on> <post_on> <comment_on> <like_save_on> <sub_on> <user_weight> <post_weight> <comment_weight> <like_save_weight> <sub_weight>'
    """
    help = 'Simulate life in the blog'

    def add_arguments(self, parser):
        """Добавляет аргументы"""

        parser.add_argument('seconds', type=float, help=u'Time between actions')

        parser.add_argument('user_on', type=int, )
        parser.add_argument('post_on', type=int, )
        parser.add_argument('comment_on', type=int, )
        parser.add_argument('like_save_on', type=int, )
        parser.add_argument('sub_on', type=int, )

        parser.add_argument('user_weight', type=float, )
        parser.add_argument('post_weight', type=float, )
        parser.add_argument('comment_weight', type=float, )
        parser.add_argument('like_save_weight', type=float, )
        parser.add_argument('sub_weight', type=float, )

    def handle(self, *args, **kwargs):
        """Принимает аргументы и на их основании запускает функцию случайного выбора действий, совершающихся пользователями"""
        seconds = kwargs['seconds']

        actions_dict = {
            'user': [kwargs['user_on'], kwargs['user_weight']],
            'post': [kwargs['post_on'], kwargs['post_weight']],
            'comment': [kwargs['comment_on'], kwargs['comment_weight']],
            'like_save': [kwargs['like_save_on'], kwargs['like_save_weight']],
            'sub': [kwargs['sub_on'], kwargs['sub_weight']],
        }

        actions = [i for i in actions_dict if actions_dict[i][0] == 1]
        weights = [actions_dict[i][1] for i in actions_dict if actions_dict[i][0] == 1]

        logger.info(actions_dict)

        while True:
            time.sleep(seconds)
            user = random.choice(User.objects.all())
            post = random.choice(News.objects.all())

            action = random.choices(population=actions, weights=weights)

            if action == ['user']:
                self.create_user()
            elif action == ['post']:
                self.add_post(user)
            elif action == ['comment']:
                self.add_comment(user, post)
            elif action == ['like']:
                self.like_or_save_post(user, post)
            elif action == ['sub']:
                self.subscribe(user)

    def create_user(self):
        """Создание пользователя"""

        user_url = 'https://randomuser.me/api/'
        user_response = requests.get(user_url)
        user_data = json.loads(user_response.text)
        first_name = user_data['results'][0]['name']['first']
        last_name = user_data['results'][0]['name']['last']
        username = f'{first_name}{last_name}'

        actions_username = random.choices(population=[1, 2, 3, 4])

        if actions_username == [1]:
            username = f"{first_name}{last_name}"
        elif actions_username == [2]:
            username = f"{first_name}{last_name}{user_data['results'][0]['dob']['date'].split('-')[0]}"
        elif actions_username == [3]:
            username = f"{user_data['results'][0]['login']['username']}"
        elif actions_username == [4]:
            username = f'{first_name}{last_name}'

        try:
            user = User.objects.create(
                username=username,
                email=f"{first_name[0].lower()}.{last_name.lower()}@example.com",
                password='test',
                first_name=first_name,
                last_name=last_name,
            )
            user.save()

            img_url = 'https://picsum.photos/200'
            img_response = requests.get(img_url)
            os.mkdir(f'media/profile_images/{user.id}')
            image_path = f'profile_images/{user.id}/{get_random_string()}.jpg'

            with open(f'media/{image_path}', 'wb') as file:
                file.write(img_response.content)

            profile = Profile.objects.create(
                user=user,
                profile_img=image_path
            )
            profile.save()
            logger.info(f"created new user: {user.username}, id: {user.id}")
        except:
            logger.info(f"something goes wrong")
            pass

    def add_post(self, user):
        """Добавление поста"""

        api_key = settings.GOOGLE_DEVELOPER_KEY
        api_service_name = "youtube"
        api_version = "v3"
        youtube = googleapiclient.discovery.build(
            api_service_name,
            api_version,
            developerKey=api_key)

        countries = [
            'AU', 'AT', 'AZ', 'AL', 'DZ', 'AR', 'AM', 'BD', 'BH', 'BY',
            'BE', 'BG', 'BO', 'BA', 'BR', 'GB', 'HU', 'VE', 'VN', 'GH',
            'GT', 'DE', 'HN', 'HK', 'GR', 'GE', 'DK', 'DO', 'EG', 'ZW',
            'IL', 'IN', 'ID', 'JO', 'IQ', 'IE', 'IS', 'ES', 'IT', 'YE',
            'KZ', 'KH', 'CA', 'QA', 'KE', 'CY', 'TW', 'CO', 'CR', 'KW',
            'LA', 'LV', 'LB', 'LY', 'LT', 'LI', 'LU', 'MK', 'MY', 'MT',
            'MA', 'MX', 'MD', 'MN', 'NP', 'NG', 'NL', 'NI', 'NZ', 'NO',
            'AE', 'OM', 'PK', 'PA', 'PG', 'PY', 'PE', 'PL', 'PT', 'PR',
            'KR', 'RU', 'RO', 'SV', 'SA', 'SN', 'RS', 'SG', 'SK', 'SI',
            'US', 'TH', 'TZ', 'TN', 'TR', 'UG', 'UA', 'UY', 'PH', 'FI',
            'FR', 'HR', 'ME', 'CZ', 'CL', 'CH', 'SE', 'LK', 'EC', 'EE',
            'ZA', 'JM', 'JP'
        ]

        country = random.choice(countries)

        response = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode=f"{country}",
            maxResults=10
        ).execute()

        videos = response.get('items')
        video = random.choice(videos)
        video_title = video['snippet']['title']
        video_desc = video['snippet']['description']
        video_id = video['id']

        content = f'{video_title}\nhttps://www.youtube.com/watch?v={video_id}\n{"*" * 50}\n\n{video_desc}\n'

        if user.username in ['admin', 'moderator']:
            pass
        else:
            post = News.objects.create(
                author=user,
                title=video_id,
                content=content,
                is_active=True,
            )
            post.save()
            logger.info(f"{user} add post {post.id}")

    def add_comment(self, user, post):
        """Добавление комментария"""

        api_key = settings.GOOGLE_DEVELOPER_KEY
        api_service_name = "youtube"
        api_version = "v3"
        youtube = googleapiclient.discovery.build(
            api_service_name,
            api_version,
            developerKey=api_key)

        if post.title:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=f"{post.title}",
            ).execute()

            comments = response.get('items')
            comment = random.choice(comments)
            text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        else:
            text = 'test'

        if user.username in ['admin', 'moderator']:
            pass
        else:
            comment = Comment.objects.create(
                user=user,
                news=post,
                text=text,
            )
            comment.save()
            post.views_count += 1
            post.save()
            logger.info(f"{user} add comment '{text}' ({comment.id}) for post {post.id}")

    def like_or_save_post(self, user, post):
        """Лайк или сохранение поста"""

        if user.username in ['admin', 'moderator']:
            pass
        else:
            res = random.choices(population=['like', 'save'], weights=[0.7, 0.3])

            if res == ['like']:
                if user in post.likes.all():
                    post.likes.remove(user)
                    logger.info(f"{user} disliked post {post.id} created by {post.author} ")
                else:
                    post.likes.add(user)
                    logger.info(f"{user} liked post {post.id} created by {post.author} ")
            else:
                if user in post.likes.all():
                    post.saves.remove(user)
                    logger.info(f"{user} unsaved post {post.id} created by {post.author} ")
                else:
                    post.saves.add(user)
                    logger.info(f"{user} saved post {post.id} created by {post.author} ")

    def subscribe(self, user):
        """Подписка пользователя"""

        if user.username in ['admin', 'moderator']:
            pass
        else:
            user_for_sub = random.choice(User.objects.all())
            if user in user_for_sub.profile.subscribers.all():
                user_for_sub.profile.subscribers.remove(user)
            else:
                user_for_sub.profile.subscribers.add(user)
            user_for_sub.profile.save()
            logger.info(f"{user} subscribed to {user_for_sub}")
