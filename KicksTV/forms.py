from django import forms
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.models import User

class UserProfileRegistrationForm(RegistrationFormUniqueEmail):
    profileImage = forms.ImageField(label='Profile Picture', required=False)
    location = forms.CharField(label=(u'Location'), help_text='Not required', max_length=30, required=False)
    bio = forms.CharField(label=(u'Bio'), help_text='Not required', widget=forms.Textarea, max_length=500, required=False)

    class Meta:
    	model = User
    	fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profileImage', 'location', 'bio']
    
