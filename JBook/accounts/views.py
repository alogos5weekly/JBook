from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import uuid

# Create your views here.
from blog.models import Post
from . import models
from .forms import UserCreateForm, UserForm, UserProfileForm

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class UserProfileView(DetailView):
    template_name = 'accounts/user_profile.html'
    model = models.UserProfile
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        temp = False
        if models.Followers.objects.filter(user=context['profile'], follows=self.request.user.profile).exists():
            temp = True
        context['is_follower'] = temp
        return context


@login_required
def profile_redirector(request):
    return redirect('accounts:profile', username=request.user.username)

class UserProfileUpdateView(UpdateView):

    template_name = 'accounts/edit_profile.html'
    form_class = UserForm
    form_class_2 = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.request.user)
        if 'form2' not in context:
            context['form2'] = self.form_class_2(instance=self.request.user.profile)  # noqa
        return context

    def get(self, request, *args, **kwargs):
        super(UserProfileUpdateView, self).get(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(instance=self.request.user)
        form2 = self.form_class_2(instance=self.request.user.profile)

        return self.render_to_response(self.get_context_data(
            form=form, form2=form2
        ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.request.user)
        form2 = self.form_class_2(request.POST, request.FILES,
                                  instance=self.request.user.profile)

        if form.is_valid() and form2.is_valid():
            form.save()
            data = form2.save(commit=False)
            if request.FILES.get('avatar', None):
                data.avatar = request.FILES['avatar']
                data.avatar.name = '{0}_p.jpg'.format(str(uuid.uuid4()))
            data.save()
            return redirect('accounts:user_profile')
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
                )

    def get_object(self, queryset=None):
        return self.request.user

@login_required
def follow(request, pk):
    # print(request.user.profile)
    models.Followers.objects.get_or_create(
        user = models.UserProfile.objects.get(pk=pk),
        follows = request.user.profile,
    )
    return redirect('accounts:profile', username=models.UserProfile.objects.get(pk=pk).user.username)

@login_required
def unfollow(request, pk):
    profile = models.UserProfile.objects.get(pk=pk)
    models.Followers.objects.filter(user=profile, follows=request.user.profile).delete()
    return redirect('accounts:profile', username=models.UserProfile.objects.get(pk=pk).user.username)



def about(request, pk):
    return redirect('accounts:profile',
        username=models.UserProfile.objects.get(pk=pk).user.username
    )
