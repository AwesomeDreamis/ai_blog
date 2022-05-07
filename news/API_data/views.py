from app_news_board.models import News, Images, Comment
from app_users.models import Profile
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from API_data.features import CustomPagination
from API_data.serializers import UserSerializer, ProfileSerializer, NewsSerializer, ImagesSerializer, CommentSerializer
from django.core.exceptions import PermissionDenied


class UserAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    """API представление для получения списка пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get(self, request):
        """Получение данных с сервера"""
        return self.list(request)

    def post(self, request, format=None):
        """Передача данных на сервер. Создание объекта"""
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            return self.create(request)

class UserDetailAPI(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """API представление для получения детальной информации о пользователе,
    а также для его редактирвоания и удаления"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """Получение объекта"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Изменение объекта"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаление объекта"""
        return self.destroy(request, *args, **kwargs)

#################################################################################


class ProfileAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    """API представление для получения списка профилей"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = CustomPagination

    def get(self, request):
        """Получение данных с сервера"""
        return self.list(request)

    def post(self, request, format=None):
        """Передача данных на сервер. Создание объекта"""
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            return self.create(request)


class ProfileDetailAPI(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """API представление для получения детальной информации о профиле,
    а также для его редактирвоания и удаления"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        """Получение объекта"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Изменение объекта"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаление объекта"""
        return self.destroy(request, *args, **kwargs)

#################################################################################


class PostAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    """API представление для получения списка новостей"""

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = CustomPagination

    def get(self, request):
        """Получение данных с сервера"""
        return self.list(request)

    def post(self, request, format=None):
        """Передача данных на сервер. Создание объекта"""
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            return self.create(request)


class PostDetailAPI(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """API представление для получения детальной информации о новости,
    а также для его редактирвоания и удаления"""

    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        """Получение объекта"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Изменение объекта"""
        if request.user.id == request.data['author'] \
                or request.user.groups.filter(name='moderators').exists():
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        """Удаление объекта"""
        if request.user.id == request.data['author'] \
                or request.user.groups.filter(name='moderators').exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied

#################################################################################


class ImagesAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    """API представление для получения списка изображений"""

    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    pagination_class = CustomPagination

    def get(self, request):
        """Получение данных с сервера"""
        return self.list(request)

    def post(self, request, format=None):
        """Передача данных на сервер. Создание объекта"""
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            return self.create(request)


class ImagesDetailAPI(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """API представление для получения детальной информации об изображении,
    а также для его редактирвоания и удаления"""

    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

    def get(self, request, *args, **kwargs):
        """Получение объекта"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Изменение объекта"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаление объекта"""
        return self.destroy(request, *args, **kwargs)

#################################################################################


class CommentAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    """API представление для получения списка комментариев"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get(self, request):
        """Получение данных с сервера"""
        return self.list(request)

    def post(self, request, format=None):
        """Передача данных на сервер. Создание объекта"""
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            return self.create(request)


class CommentDetailAPI(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """API представление для получения детальной информации о комментарии,
    а также для его редактирвоания и удаления"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        """Получение объекта"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Изменение объекта"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаление объекта"""
        return self.destroy(request, *args, **kwargs)
