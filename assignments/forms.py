from django import forms
from django.contrib.auth.models import User


from .models import Module, courseWork


class ModuleForm(forms.ModelForm):
	module_date = forms.DateField(widget=forms.SelectDateWidget)
    
	class Meta:
		model = Module
		fields = ['module_name', 'module_id', 'module_date']

class CourseWorkForm(forms.ModelForm):
	coarseWork_date = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = courseWork
		fields = ['courseWork_title', 'courseWork_file']

