from django.contrib import admin
from app_news_board.models import News, Images
from app_news_board.models import Comment


# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment


class NewsImagesInline(admin.TabularInline):
    model = Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'news']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'author']
    search_fields = ['title', 'content', 'author']
    inlines = [NewsImagesInline, CommentInLine]

    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)

    mark_as_active.short_description = 'перевести в статус активно'
    mark_as_inactive.short_description = 'перевести в статус неактивно'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    def get_text(self):
        if len(self.text) > 15:
            return self.text[:15] + '...'
        else:
            return self.text

    get_text.short_description = 'text'

    list_display = ['user', get_text]
    list_filter = ['user']
    search_fields = ['user', 'text']

    actions = ['delete_comment']

    def delete_comment(self, request, queryset):
        queryset.update(text='Удалено администратором')

    delete_comment.short_description = 'удалить комментарий'

