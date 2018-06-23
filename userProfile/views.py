from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.datastructures import MultiValueDictKeyError

from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth.models import User, Group

from .models import Profile
from .forms import ProfileSettings

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.


def userProfile(request, user):
	user = get_object_or_404(User, username=user)
	
	if user.profile:
		context = {
			'user': user,
		}
		return render(request, 'userProfile/index.html', context)
	else:
		return render(request, 'default-form.html')

def userProfileSettings(request, user):
	if not request.user.username == user:
		return HttpResponse('<h1>Cannot edit other uses settings</h1>')
	else:
		user = get_object_or_404(User, username=user)
		form = ProfileSettings(request.POST or None, request.FILES or None, instance=user.profile)
		if form.is_valid():

			user.first_name = form.cleaned_data['firstName']
			user.last_name = form.cleaned_data['lastName']
			profile = form.save(commit=False)
			profile.user = user

			try:
				profile.profile_image = request.FILES['profile_image']
				file_type = profile.profile_image.url.split('.')[-1]
				file_type = file_type.lower()
				if file_type not in IMAGE_FILE_TYPES:
					context = {
						'profile': profile,
						'form': form,
						'error_message': 'Image file must be PNG, JPG or JPEG!',
					}
					return render(request, 'default-form.html', context)
			except MultiValueDictKeyError:
				profile.profile_image = profile.profile_image

			profile.save()
			user.save()
			messages.success(request, "Successfully Made Changes!")
			return HttpResponseRedirect(reverse('profile:index', args=[user]))
		context = {
			'formTitle': 'Profile Settings',
			'form': form,
		}

		return render(request, 'default-form.html', context)
