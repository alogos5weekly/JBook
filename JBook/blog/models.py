from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField, get_thumbnail

User = get_user_model()


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

class Category(models.Model):
    title = models.CharField(max_length=20)
    description = RichTextUploadingField(blank=True, null=True)
    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = RichTextUploadingField(blank=False, null=True)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100, unique = True)
    overview = RichTextUploadingField()
    created_at = models.DateTimeField(editable=False)
    published_at = models.DateTimeField( null=True)
    updated_at = models.DateTimeField()
    content = RichTextUploadingField(blank=False, null=True)
    # comment_count = models.IntegerField(default = 0)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    thumbnail = ImageField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(blank=True, default=False)
    slug = models.SlugField(max_length = 250, null = True, blank = True, unique = True)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # if self.thumbnail:
        #     self.im = get_thumbnail(self.thumbnail, format='JPEG')
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Post, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={
            'slug': self.slug,
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def like_count(self):
        return Like.objects.filter(post=self).count()
