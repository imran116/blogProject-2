from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_home'),
    path('profile/<int:profile_id>/', views.profile_setting, name='profile'),
    path('profile-change/', views.profile_change, name='profile_change'),
    path('profile-picture/', views.profile_info, name='profile-picture'),
    path('write-blog/', views.CreateBlog.as_view(), name='create-blog'),
    path('blog-details/<slug:slug>/', views.blog_details, name='blog-details'),
    path('blog-comment/<int:blog_id>/', views.comment_view, name='blog-comment'),
    path('blog-like/<int:blog_id>/', views.like, name='blog-like'),
    path('blog-unlike/<int:blog_id>/', views.unlike, name='blog-unlike'),
    path('search-blog/', views.search_blog, name='search-blog'),

]
