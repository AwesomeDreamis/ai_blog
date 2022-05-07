from django import forms
from app_news_board.models import News, Images, Comment
from django.forms import Textarea


class NewsForm(forms.ModelForm):
    """Форма новости"""

    title = forms.CharField(max_length=1500, required=False)
    likes = forms.IntegerField(required=False)
    saves = forms.IntegerField(required=False)

    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget = Textarea(attrs={'class': 'create_post_content'})


class NewsImagesForm(forms.ModelForm):
    """Форма изображений для новости"""

    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'create_news_images',
                                                                                     'id': 'news-imgs',
                                                                                     'multiple': True}))

    class Meta:
        model = Images
        fields = ['image', ]


class CommentForm(forms.ModelForm):
    """Форма комментария"""

    text = forms.CharField(required=True)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'create_comment_img',
                                                                                    'id': 'comment-img',
                                                                                    'placeholder': 'upload image'}))

    class Meta:
        model = Comment
        fields = ('text', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'class': 'create_comment_text',
                                                     'placeholder': 'write your comment...'})

