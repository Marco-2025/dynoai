from django.db import models
from django import forms

# Create your models here.
class ImageUpload(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='')
