from django.contrib import admin
from .models import Folder, SubFolder, File


# Register your models here.

admin.site.register(Folder)
admin.site.register(SubFolder)