from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
