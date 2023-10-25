from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
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
  
class CustomUserManager(BaseUserManager):
  def create_user(self, email, username, password=None, **extra_fields):
    if not email:
      raise ValueError('The Email field must be set')
    email = self.normalize_email(email)
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    
    user = self.model(email=email, username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, username, password=None, **extra_fields):
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    
    return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser):
  username = models.CharField(
    max_length=150,
    unique=True,
    error_messages={'이미 사용 중인 사용자 이름입니다'}
  )
  email = models.EmailField(unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(null=True, blank=True)
  
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  objects = CustomUserManager()
  
  USERNAME_FIELD = 'username'
  
  def __str__(self):
    return self.username
