from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Folder(models.Model):
	folder_name = models.CharField(max_length=100)
	folder_path = models.CharField(max_length=100)
	number_of_files = models.IntegerField(default=0)

	def __str__(self):
		return self.folder_name


class SubFolder(models.Model):
	parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
	sub_folder =  models.ForeignKey('self', null=True)
	sub_folder_name = models.CharField(max_length=100)
	sub_folder_path = models.CharField(max_length=100)
	sub_folder_files = models.IntegerField(default=0)

	def __str__(self):
		return self.sub_folder_name

class File():
	file_sub_folder = models.ForeignKey(SubFolder, on_delete=models.CASCADE)
	file_name = models.CharField(max_length=100)