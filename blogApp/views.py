import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView

from loginApp.models import UserProfile
from blogApp.models import Blog, Comment

from loginApp.forms import ProfileChangeForm, ProfilePictureForm
from blogApp.forms import CommentForm


# Create your views here.

class BlogListView(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blogApp/blog_index.html'


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


class CreateBlog(CreateView):
    model = Blog
    fields = ('blog_image', 'blog_title', 'blog_content',)
    template_name = 'blogApp/write_blog.html'

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj.author = self.request.user
        title = form_obj.blog_title
        form_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        form_obj.save()
        return HttpResponseRedirect(reverse('index'))


def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)

    return render(request, 'blogApp/blog_details.html', context={'blog': blog})


def comment_view(request, blog_id):
    if request.method == 'POST':
        slug = Blog.objects.get(pk=blog_id)
        slugg = slug.slug
        print(slugg)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.data['comment']
            Comment.objects.create(
                user=request.user,
                blog_id=blog_id,
                comment=comment,
            ).save()
            return HttpResponseRedirect(reverse('blog_app:blog-details',kwargs={'slug':slugg}))

    return render(request, 'blogApp/blog_details.html')



