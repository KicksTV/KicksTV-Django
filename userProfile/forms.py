from django import forms

from django.contrib.auth.models import User

from .models import Profile

class ProfileSettings(forms.ModelForm):

	firstName = forms.CharField(label=(u'First Name'), help_text='Not required', max_length=30, required=False)
	lastName = forms.CharField(label=(u'Last Name'), help_text='Not required', max_length=30, required=False)

	class Meta:
		model = Profile
		fields = ['firstName', 'lastName', 'profile_image', 'bio', 'location']