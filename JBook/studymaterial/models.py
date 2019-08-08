from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.contrib.auth import get_user_model
from sorl.thumbnail import ImageField, get_thumbnail

User = get_user_model()


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
    document = models.FileField(upload_to='docs/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=3, choices=CATEGORY)
    thumbnail = ImageField(blank=True, null=True)
    slug = models.SlugField(max_length = 250, null = True, blank = True, unique = True)

    def __str__(self):
        return self.name

    def save(self):
        slug_string = "%s-%s" % (self.name, self.pk)
        self.slug = slugify(slug_string)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('studymaterial:document_detail', kwargs={
            'slug': self.slug,
        })
