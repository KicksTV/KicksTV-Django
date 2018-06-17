from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.conf import settings

from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db import models

import os
import sys
import shutil



# Create your models here.

def upload_location(instance, filename):
    folder = instance.slug.replace("_", "/")
    return "project_images/%s/%s" %(folder, filename)


class Project(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	name = models.CharField(max_length=60)
	image = models.FileField(upload_to=upload_location, 
		null=False, 
		blank=False,)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	slug = models.SlugField(max_length=60, unique=True)
	on_going = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	description = models.CharField(max_length=70)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("blogs:project-detail", kwargs={"slug": self.slug})



class Post(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	title = models.CharField(max_length=60)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	draft = models.BooleanField(default=True)
	publish = models.DateField(auto_now=False, auto_now_add=False)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blogs:post-detail", kwargs={
			"slug": self.project.slug,
			"post_id": self.id,
			})



def create_slug(instance, new_slug=None):
	slug = "%s_%s" %(instance.user, slugify(instance.name))
	
	if new_slug is not None:
		slug = new_slug

	qs = Project.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s_%s-%s" %(instance.user, slugify(instance.name),qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_project_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_project_receiver, sender=Project)

@receiver(models.signals.post_delete, sender=Project)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            print(instance.image.path)
            os.remove(instance.image.path)
            try:
                folder = instance.image.path.rsplit('/', 1)
                shutil.rmtree(folder[0])
            except OSError, e:
                print("Error: %s - %s." % (e.filename, e.strerror))
