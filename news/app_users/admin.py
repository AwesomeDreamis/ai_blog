from django.contrib import admin
from app_users.models import Profile
from django.contrib.auth.models import User


# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'news_count', 'is_banned', 'profile_img', 'sub_count', 'subs_count']
    list_filter = ['is_banned', ]
    actions = ['mark_as_banned', 'mark_as_unbanned']
    search_fields = ['city']


    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)

    def mark_as_non_verified(self, request, queryset):
        queryset.update(is_verified=False)

    mark_as_verified.short_description = 'ban'
    mark_as_non_verified.short_description = 'unban'
