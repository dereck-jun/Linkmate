from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os


# Create your models here.
class Tag(models.Model):
  name = models.CharField(max_length=50) #, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
  author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 사용자와 연결
  
  # 기타 코드...
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name, allow_unicode=True)
    super(Tag, self).save(*args, **kwargs)
  
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return f'/bookmark/tag/{self.slug}/'
  


class Bookmark(models.Model):
  title = models.CharField(max_length=60)
  url = models.URLField(max_length=120)
  head_image = models.ImageField(upload_to='bookmark/images/%Y/%m/%d/', blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
  tags = models.ManyToManyField(Tag, blank=True)
  
  def __str__(self):
    return f'[{self.pk}]{self.title} :: {self.author}'
  
  def get_absolute_url(self):
    return f'/bookmark/{self.pk}/'
  
  # def get_file_name(self):
  #   return os.path.basename(self.file_upload.name)
  #
  # def get_file_ext(self):
  #   return self.get_file_name().split('.')[-1]