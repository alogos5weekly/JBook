from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(models.Model):
    CATEGORY = (
        ('CS', 'Class Notes'),
        ('ME', 'MTT papers'),
        ('EE', 'RTU papers'),
        ('ECE', 'Coding related stuff'),
        ('CE', 'Book'),
        ('IT', 'magazines'),

    )
    title = models.CharField(max_length = 200)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
