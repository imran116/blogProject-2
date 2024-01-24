from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.blog, name='blog_home'),
    path('profile/', views.profile_setting, name='profile'),
    path('profile-change/', views.profile_change, name='profile_change'),
    path('profile-picture/', views.profile_info, name='profile-picture'),

]
