from django import forms
# from django.forms import Textarea


class UploadPostForm(forms.Form):
    file = forms.FileField()
