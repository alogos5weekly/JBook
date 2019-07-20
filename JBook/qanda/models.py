from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
User = get_user_model()
class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=100)
    question_text = RichTextUploadingField(blank=False, null=True)
    date_posted = models.DateTimeField(auto_now_add = True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=40)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.question_title)
        super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
    aid = models.AutoField(primary_key = True)
    qid = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer_text = RichTextUploadingField(blank=False, null=True)
    date_posted = models.DateTimeField(auto_now_add = True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
