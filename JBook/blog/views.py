from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CommentForm, PostForm
from .models import Post, PostView, Comment, Like
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponseRedirect

User = get_user_model()

def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  ###https://stackoverflow.com/questions/5959779/what-is-context-object-name-in-django-views
    paginate_by = 4

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['t'] = 0
        return context

    def get_queryset(self):
        return Post.objects.filter(published_at__lte=timezone.now()).order_by('-published_at')

class UserPosts(LoginRequiredMixin ,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        print(13)
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        context['t'] = 1
        return context

    ### prefetch_related:  https://kite.com/python/docs/django.db.models.query.QuerySet.prefetch_related
    def get_queryset(self):
        print(12)
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))#https://docs.djangoproject.com/en/dev/ref/models/querysets/#get
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()


class DraftListView(LoginRequiredMixin, ListView):
    template_name = 'blog/post_draft_list.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        try:
            self.post_user = self.request.user
        except:
            raise Http404
        else:
            return self.post_user.posts.filter(published_at__isnull=True).order_by('created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form = CommentForm()

    # def get_queryset(self):
    #     return super().get_queryset().filter(published_at__isnull=False)

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-published_at')[:3]
        context = super().get_context_data(**kwargs)
        temp = False
        if Like.objects.filter(user=self.request.user, post=self.get_object()).exists():
            temp = True
        context['is_liked'] = temp
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context
    ## post method overriding
    ## if we do not probvide implementation of this method or get method we
    ## have to define "slug_field = 'title'" & "slug_url_kwargs = 'title'"
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect('blog:post_detail', slug=post.slug)


class PostCreateView(LoginRequiredMixin , CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def get_success_url(self):
        if 'draft' in self.request.POST:
            return reverse('blog:draft_posts')
        return super().get_success_url()


    def form_valid(self, form):
        self.form = form
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         post = self.get_object()
    #         form.instance.user = request.user
    #         form.instance.post = post
    #         form.save()
    #         return redirect('blog:post_detail', slug=post.slug)
    #

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/edit_post.html'
    form_class = PostForm

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        post.delete()
        return redirect('blog:post_list')
    else:
        return redirect('blog:post_detail', slug=slug)

@login_required
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        post.publish()
        return redirect('blog:post_detail', slug=slug)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def comment_remove(request, pk):
    comment = Comment.objects.get(pk=pk)
    post_slug = comment.post.slug
    if request.user == comment.user:
        comment.delete()
    return redirect('blog:post_detail', slug=post_slug)


@login_required
def like(request, slug):
    post = Post.objects.get(slug=slug)
    new_like, created = Like.objects.get_or_create(user=request.user, post=post)
    return redirect('blog:post_detail', slug=slug)
