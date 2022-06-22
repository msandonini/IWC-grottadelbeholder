"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views
from .views import *

app_name = "grottadelbeholder"
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create', CreateContentView.as_view(), name='create'),
    path('add', AddContentView.as_view(), name='addContent'),
    path('usercontent', UserContentView.as_view(), name='usercontent'),
    path('review', ReviewView.as_view(), name='review'),
    path('login', LoginView.as_view(), name='login'),
    path('signin', SigninView.as_view(), name='signin'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('info', InfoView.as_view(), name='info'),
    path('user', UserView.as_view(), name='user'),
    path('admin', AdminView.as_view(), name='admin')
]
