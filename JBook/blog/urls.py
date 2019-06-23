from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/drafts/', views.DraftListView.as_view(), name='drafts_posts'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/like/', views.like, name='post_like'),
    path('post/<slug:slug>/publish/',views.post_publish, name='publish_post'),
    path('post/<slug:slug>/delete/',views.post_delete, name='post_delete'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/comment/delete/', views.comment_remove, name='delete_comment'),
    path('post/<str:username>/posts/', views.UserPosts.as_view(), name='user_posts'),

]
