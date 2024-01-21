from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.blog, name='blog_home'),
    path('profile', views.profile_setting, name='profile'),

]
