from django import forms
from django.contrib.auth.models import User

from .models import Gallery, Image


class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ['gallery_title', 'gallery_date', 'gallery_image', 'gallery_description']

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image_title', 'image_image']

