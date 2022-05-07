from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .forms import RegisterForm, ProfileEditForm
from app_users.models import Profile
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
import logging


logger = logging.getLogger(__name__)


class Login(LoginView):
    """Представление логина"""
    template_name = 'users/login.html'


class Logout(LogoutView):
    """Представление разлогина"""
    next_page = '/'


class RegisterView(View):
    """Представление регистрации"""

    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'email or username is already taken ')
            return redirect('register')


# class ProfileView(DetailView, UserPassesTestMixin):
#     template_name = 'users/profile.html'
#     model = Profile
#
#     def test_func(self):
#         profile = self.get_object()
#         return profile.user == self.request.user

class ProfileView(View, UserPassesTestMixin):
    """Представление просмотра профиля"""

    def get(self, request, pk):
        if not self.request.user.id == pk:
            raise PermissionDenied

        user_data = User.objects.get(id=pk)

        try:
            profile_data = user_data.profile
            user_form = RegisterForm(instance=user_data)
            profile_form = RegisterForm(instance=profile_data)

            if not request.user == user_data:
                raise PermissionDenied()

            return render(request, 'users/profile.html', context={'user_form': user_form,
                                                                  'profile_form': profile_form,
                                                                  'user': user_data,
                                                                  'profile': profile_data,
                                                                  'profile_id': pk,
                                                                  })
        except:
            profile_data = Profile.objects.create(
                user=user_data,
            )
            profile_data.save()
            user_form = RegisterForm(instance=user_data)
            profile_form = RegisterForm(instance=profile_data)

            if not request.user == user_data:
                raise PermissionDenied()

            return render(request, 'users/profile.html', context={'user_form': user_form,
                                                                  'profile_form': profile_form,
                                                                  'user': user_data,
                                                                  'profile': profile_data,
                                                                  'profile_id': pk,
                                                                  })


class ProfileUpdateView(View):
    """Представление редактирования профиля"""

    def get(self, request, profile_id):
        if not self.request.user.id == profile_id:
            raise PermissionDenied

        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'profile_img': user_profile.profile_img,
            'profile_head_img': user_profile.profile_head_img,

        }

        form = ProfileEditForm(default_data)

        return render(request, 'users/profile_edit.html', {'form': form, 'user': user})

    def post(self, request, profile_id):
        if not self.request.user.id == profile_id:
            raise PermissionDenied

        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        form = ProfileEditForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.username = form.cleaned_data['username']
                old_email = user.email
                user.email = form.cleaned_data['email']

                if form.cleaned_data['profile_img']:
                    user_profile.profile_img = form.cleaned_data['profile_img']
                if form.cleaned_data['profile_head_img']:
                    user_profile.profile_head_img = form.cleaned_data['profile_head_img']

                if user.email == old_email\
                        or not User.objects.filter(email=user.email).exists():
                    user.save()
                    user_profile.save()
                    return redirect('profile', profile_id)
                else:
                    raise
            except:
                return redirect('profile_edit', profile_id)
        else:
            return redirect('profile_edit', profile_id)
