from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.shortcuts import get_object_or_404

from django.utils.text import slugify


import os
import sys
import shutil

 
# Create your models here.
def upload_location(instance, filename):
    folder = instance.slug.replace("_", "/")
    return "gallery_images/%s/%s" %(folder, filename)

class Gallery(models.Model):
    user = models.ForeignKey(User, default=1)
    gallery_title = models.CharField(max_length=25)
    gallery_date = models.DateField(null=False, blank=False)
    gallery_image = models.ImageField(
        upload_to=upload_location, 
        null=False, 
        blank=False,
        height_field="height_field",
        width_field="width_field",
        )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    slug = models.SlugField(max_length=40, unique=True)
    gallery_description = models.CharField(max_length=70)
    is_favorite = models.BooleanField(default=False)
    is_homepage_gallery = models.BooleanField(default=False)

    def __unicode__(self):
        return self.gallery_title

    def __str__(self):
        return self.gallery_title

    def get_absolute_url(self):
        return reverse("gallerys:user-gallery-detail", kwargs={
            "slug": self.slug,
            "gallery_user": self.user,
            })

class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image_title = models.CharField(max_length=25)
    image_image = models.ImageField(
        upload_to=upload_location,
        height_field="height_field",
        width_field="width_field",
        )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    slug = models.SlugField(max_length=40)

    def __unicode__(self):
        return self.image_title

    def __str__(self):
        return self.image_title



# Creating slugs before saving
def create_slug(instance, new_slug=None):
    slug = "%s_%s" %(instance.user, slugify(instance.gallery_title))
    if new_slug is not None:
        slug = new_slug
    qs = Gallery.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s_%s-%s" %(instance.user, slugify(instance.gallery_title),qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_gallery_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    elif not instance.slug == slugify(instance.user) + "" + slugify(instance.gallery_title): 
        instance.slug = create_slug(instance)

def pre_save_image_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        gallery = Gallery.objects.get(id=instance.gallery.id)
        instance.slug = "%s_%s" %(gallery.user,slugify(gallery.gallery_title))


# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=Gallery)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.gallery_image:
        if os.path.isfile(instance.gallery_image.path):
            os.remove(instance.gallery_image.path)
            try:
                folder = instance.gallery_image.path.rsplit('/', 1)
                shutil.rmtree(folder[0])
            except OSError, e:
                print("Error: %s - %s." % (e.filename, e.strerror))


def auto_delete_file_on_change(sender, instance, *args, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        print("instance.pk is null")
        return

    if instance.gallery_title:
        old_gallery = get_object_or_404(Gallery, id=instance.pk)
        if instance.gallery_title == old_gallery.gallery_title:
            return

    gallery_path = str(instance.gallery_image).split("/")
    old_file = gallery_path[1] + "/" + gallery_path[2]
    new_file = instance.slug.replace("_", "/")
    
    if not old_file == new_file:
        folder_path_to_change = str(instance.gallery_image.path).rsplit('/', 1)
        folder_path = str(instance.gallery_image.path).rsplit('/', 2)
        new_folder_name = str(new_file).rsplit('/', 1)
        os.rename(folder_path_to_change[0], folder_path[0] + "/" + new_folder_name[1])
        instance.gallery_image = gallery_path[0] + "/" + gallery_path[1] + "/" + new_folder_name[1] + "/" + gallery_path[3]

        all_images = Image.objects.filter(gallery=instance)
        if all_images:
            for image in all_images:
                if not os.path.isfile(image.image_image.path):
                    image_path = str(image.image_image).split("/")
                    print(image_path[0] + "/" + image_path[1] + "/" + new_folder_name[1] + "/" + image_path[3])
                    image.image_image = image_path[0] + "/" + image_path[1] + "/" + new_folder_name[1] + "/" + image_path[3]
                    image.save()


pre_save.connect(pre_save_gallery_receiver, sender=Gallery)
pre_save.connect(pre_save_image_receiver, sender=Image)
pre_save.connect(auto_delete_file_on_change, sender=Gallery)