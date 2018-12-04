from django.urls import path, re_path
from django.conf.urls import url
from . import views as account_views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', account_views.home, name='accounts-home'),
    path('register/', account_views.register, name='register'),
    url(r'^profile/', account_views.profile, name='profile'),
    path('allfiles/', account_views.allfiles, name='allfiles'),
    url(r'^delete/(?P<file>.*)', account_views.delete, name='delete'),
    url(r'^profile2/(?P<paths>.*)', account_views.profile2, name='profile2'),
    path('login/', account_views.user_login, name='login'),
    path('logout/', account_views.user_logout, name='logout'),
    path('upload/', account_views.upload, name='upload'),
]
