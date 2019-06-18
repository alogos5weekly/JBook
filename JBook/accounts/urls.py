from django.urls import re_path,path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'accounts'


urlpatterns = [
    re_path(r'login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='login'),
    re_path(r'logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'signup/$', views.SignUp.as_view(), name='signup'),
    re_path(r'^@(?P<username>[\w-]+)/$', views.UserProfileView.as_view(), name='profile'),
    re_path(r'^profile/$', views.profile_redirector, name='user_profile'),
    re_path(r'^profile/update/$', views.UserProfileUpdateView.as_view(), name='user_profile_update'),
    re_path(r'^profile/(?P<pk>\d+)/follow/$', views.follow, name='follow'),
    re_path(r'^profile/(?P<pk>\d+)/unfollow/$', views.unfollow, name='unfollow'),
    re_path(r'^profile/(?P<pk>\d+)/about/$', views.about, name='about'),
    #re_path(r'^profile/(?P<pk>\d+)/posts/$', views.UserPosts.as_view(), name='user_posts'),
    #re_path(r'^profile/(?P<pk>\d+)/uploads/$', views.UserUploads.as_view(), name='user_uploads')
]
