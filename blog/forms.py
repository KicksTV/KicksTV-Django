from django import forms
from django.contrib.auth.models import User

from .models import Post, Project


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'draft', 'publish', 'content']


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'image', 'description']