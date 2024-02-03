import uuid

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView

from loginApp.models import UserProfile
from blogApp.models import Blog, Comment, Like, Unlike

from loginApp.forms import ProfileChangeForm, ProfilePictureForm
from blogApp.forms import CommentForm


# Create your views here.

class BlogListView(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blogApp/blog_index.html'


def profile_setting(request, profile_id):
    blog = Blog.objects.filter(author_id=profile_id)

    return render(request, 'blogApp/profile.html', context={'blogs': blog})


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

            return HttpResponseRedirect(reverse('blog_app:profile', kwargs={'profile_id': request.user.id}))

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
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    if already_liked:
        liked_post = True
    else:
        liked_post = False

    return render(request, 'blogApp/blog_details.html', context={'blog': blog, 'liked_post': liked_post})


def comment_view(request, blog_id):
    if request.method == 'POST':
        blog = Blog.objects.get(pk=blog_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.data['comment']
            Comment.objects.create(
                user=request.user,
                blog_id=blog_id,
                comment=comment,
            ).save()
            return HttpResponseRedirect(reverse('blog_app:blog-details', kwargs={'slug': blog.slug}))

    return render(request, 'blogApp/blog_details.html')


def like(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    unliked = Unlike.objects.filter(user=user, blog=blog)
    unliked.delete()

    if not already_liked:
        liked_post = Like(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('blog_app:blog-details', kwargs={'slug': blog.slug}))


def unlike(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    user = request.user
    unliked = Unlike(blog=blog, user=user)
    unliked.save()
    already_liked = Like.objects.filter(user=user, blog=blog)
    already_liked.delete()
    return HttpResponseRedirect(reverse('blog_app:blog-details', kwargs={'slug': blog.slug}))


def search_blog(request):
    search_text = request.GET.get('q')
    blog = Blog.objects.filter(Q(blog_title__icontains=search_text))
    number_of_blog = blog.count()
    return render(request, 'blogApp/blog_index.html', context={'blogs': blog,'number_of_blogs':number_of_blog})
