"""quantrade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^strategy01/$', views.strategy01, name='strategy01'),

    url(r'^strategy02/$', views.strategy02, name='strategy02'),
    url(r'^data_fresh/$', views.data_fresh, name='data_fresh'),

    url(r'^strategy03/$', views.strategy03, name='strategy02'),
    url(r'^strategy03_ajax_post_01/$', views.comments_upload),


]
