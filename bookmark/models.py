from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
class Bookmark(models.Model):
  title = models.CharField(max_length=60)
  url = models.URLField(max_length=120)
  
  head_image = models.ImageField(upload_to='bookmark/images/%Y/%m/%d/', blank=True)
  file_upload = models.FileField(upload_to='bookmark/files/%Y/%m/%d/', blank=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'[{self.pk}]{self.title} :: {self.author}'
  
  def get_absolute_url(self):
    return f'/bookmark/{self.pk}/'
  
  def get_file_name(self):
    return os.path.basename(self.file_upload.name)
  
  def get_file_ext(self):
    return self.get_file_name().split('.')[-1]