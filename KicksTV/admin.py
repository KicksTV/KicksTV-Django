from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileModelAdmin(admin.ModelAdmin):
	class meta:
		model = Profile

admin.site.register(Profile, ProfileModelAdmin)