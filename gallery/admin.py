from django.contrib import admin
from .models import Gallery, Image
# Register your models here.

class GalleryModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "user", "gallery_date", "is_favorite"]
	list_display_links = ["__unicode__"]
	list_filter = ["gallery_date", "is_favorite"]
	search_fields = ["gallery_title"]
	class meta:
		model = Gallery

class ImageModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "gallery", ]
	list_display_links = ["__unicode__"]
	search_fields = ["image_title", "gallery"]
	class meta:
		model = Image

admin.site.register(Gallery, GalleryModelAdmin)
admin.site.register(Image, ImageModelAdmin)