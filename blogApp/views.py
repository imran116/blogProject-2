from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from loginApp.models import UserProfile

from loginApp.forms import ProfileChangeForm, ProfilePictureForm


# Create your views here.

def blog(request):
    return render(request, 'blogApp/blog_index.html', context={'j': "hello i am form blog.page.html"})


def profile_setting(request):
    return render(request, 'blogApp/profile.html', context={})


def profile_change(request):
    current_user = request.user
    form = ProfileChangeForm(instance=current_user)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = ProfileChangeForm(instance=current_user)

    return render(request, 'blogApp/profile_change.html', context={'form': form})


@login_required
def profile_info(request):
    profile_img = False
    form = ProfilePictureForm()
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the user's existing profile picture if it exists
            existing_profile = UserProfile.objects.filter(user=request.user).first()

            if existing_profile:
                # If a profile picture exists, update it
                existing_profile.profile_picture = form.cleaned_data['profile_picture']
                existing_profile.save()
            else:
                # If no profile picture exists, create a new one
                profile_obj = form.save(commit=False)
                profile_obj.user = request.user
                profile_obj.save()

            return HttpResponseRedirect(reverse('blog_app:profile'))

    return render(request, 'blogApp/profile_pic.html', context={'form': form, 'profile_img': profile_img})
