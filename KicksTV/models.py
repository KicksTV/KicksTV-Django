from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


def upload_location(instance, filename):
    return "profile_images/%s/%s" %(instance.username, filename)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_image = models.ImageField(
        upload_to=upload_location,
        default=static('img/default-profile-image.jpg'),
        height_field="height_field",
        width_field="width_field",
        )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()