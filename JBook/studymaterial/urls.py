from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'studymaterial'

urlpatterns = [
    path('', views.PostListView.as_view(), name='document_detail'),
]
