from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group

from .models import Profile

# Create your views here.


def userProfile(request, user):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		user = get_object_or_404(User, username=user)
		profile = Profile.objects.get(user=user)

		if profile:
			context = {
				'user': user,
				'profile': profile,
			}
			return render(request, 'userProfile/user-profile.html', context)

		else:
			return render(request, 'default-form.html')