from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File as FileWrapper

from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

def upload_location(instance, filename):
    return "profile_images/%s/%s" %(instance.user.username, filename)


class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
	profile_image = models.ImageField(
		upload_to=upload_location,
		default='default-profile-image.png',
		height_field="height_field",
		width_field="width_field",
	)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Profile.objects.create(user=instance)
        p = Profile(user=instance)
        p.save()
        print(instance.profile.profile_image)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


@receiver(models.signals.pre_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	"""
	Deletes file from filesystem
	when corresponding `MediaFile` object is deleted.
	"""
	
	if instance.profile.profile_image:
		if instance.profile.profile_image == "default-profile-image.png":
			print("default image")
			return None
		# elif os.path.isfile(instance.profile.profile_image.path):
		# 	os.remove(instance.profile.profile_image.path)

