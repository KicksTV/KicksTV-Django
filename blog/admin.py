from django.contrib import admin

from .models import Post, Project

# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "updated","timestamp"]
	list_display_links = ["__unicode__"]
	list_filter = ["updated", "timestamp"]
	search_fields = ["title","content"]
	class meta:
		model = Post

class ProjectModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "user", "updated", "timestamp"]
	class meta:
		model = Project

admin.site.register(Post, PostModelAdmin)
admin.site.register(Project, ProjectModelAdmin)