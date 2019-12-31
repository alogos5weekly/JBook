from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'studymaterial'

urlpatterns = [
    path('', views.DocumentList.as_view(), name='document_list'),
    path('upload/', views.upload_document, name='upload_doc'),
    path('useful/<slug:slug>/', views.found_useful, name='useful'),
    path('unlike/<slug:slug>/', views.unlike, name='unlike'),  
]
