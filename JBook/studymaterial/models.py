from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.contrib.auth import get_user_model

from django.template.defaultfilters import slugify
from .utils import unique_slug_generator
User = get_user_model()


def get_upload_path(instance, filename):
    return "docs/{user}/{filename}".format(user=instance.uploaded_by.username, filename=filename)

class Document(models.Model):
    CATEGORY = (
        ('Class Notes', 'Class Notes'),
        ('MTT papers', 'MTT papers'),
        ('RTU papers', 'RTU papers'),
        ('Coding related stuff', 'Coding related stuff'),
        ('Book', 'Book'),
        ('magazines', 'magazines'),
        ('others', 'others')
    )
    name = models.CharField(max_length = 200)
    document = models.FileField(upload_to=get_upload_path, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30, choices=CATEGORY, null=True)
    slug = models.SlugField(max_length = 250, null = True, blank = True, unique = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            current_doc = Document.objects.get(id=self.id)
            if current_doc.document != current_doc.document:
                current_doc.document.delete(save=False)
        except:
            if not self.slug:
                self.slug = unique_slug_generator(self)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('studymaterial:document_detail', kwargs={
            'slug': self.slug,
        })

    def get_useful_count(self):
        return Useful.objects.filter(document=self).count()

    def is_liked(self, user):
        return Useful.objects.filter(document=self, person=user).exists()

class Useful(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
