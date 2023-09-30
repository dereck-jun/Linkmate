from .models import Bookmark, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
# Create your views here.

class BookmarkCreate(LoginRequiredMixin, UserPassesTestMixin ,CreateView):
  model = Bookmark
  fields = ['title', 'url', 'head_image', 'file_upload', 'category']
  
  def test_func(self):
    return self.request.user.is_superuser or self.request.user.is_staff
  
  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
      form.instance.author = current_user
      response = super(BookmarkCreate, self).form_valid(form)
      
      tags_str = self.request.POST.get('tags_str')
      if tags_str:
        tags_str = tags_str.strip()
        
        tags_str = tags_str.replace(',', ';')
        tags_list = tags_str.split(';')
        
        for t in tags_list:
          t = t.strip()
          tag, is_tag_created = Tag.objects.get_or_create(name=t)
          if is_tag_created:
            tag.slug = slugify(t, allow_unicode=True)
            tag.save()
          self.object.tags.add(tag)
      return response
    else:
      return redirect('/bookmark/')

class BookmarkList(ListView):
  model = Bookmark
  ordering = "title"
  paginate_by = 5
  
  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(BookmarkList, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Bookmark.objects.filter(category=None).count()
    
    return context
  
def category_page(request, slug):
  if slug == 'no_category':
    category = '미분류'
    bookmark_list = Bookmark.objects.filter(category=None)
  else:
    category = Category.objects.get(slug=slug)
    bookmark_list = Bookmark.objects.filter(category=category)
  
  return render(request, 'bookmark/bookmark_list.html', {
    'bookmark_list': bookmark_list,
    'categories': Category.objects.all(),
    'no_category_bookmark_count': Bookmark.objects.filter(category=None).count(),
    'category': category,
  })

def tag_page(request, slug):
  tag = Tag.objects.get(slug=slug)
  bookmark_list = tag.bookmark_set.all()
  
  return render(request, 'bookmark/bookmark_list.html', {
    'bookmark_list': bookmark_list,
    'tag': tag,
    'categories': Category.objects.all(),
    'no_category_bookmark_count': Bookmark.objects.filter(category=None).count(),
    })

  
class BookmarkDetail(DetailView):
  model = Bookmark
  
  def get_context_data(self, **kwargs):
    context = super(BookmarkDetail, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Bookmark.objects.filter(category=None).count()
    
    return context
  
  
class BookmarkUpdate(LoginRequiredMixin, UpdateView):
  model = Bookmark
  fields = ['title', 'url', 'head_image', 'file_upload', 'category', 'tags']
  
  template_name = 'bookmark/bookmark_update_form.html'
  
  def get_context_data(self, **kwargs):
    context = super(BookmarkUpdate, self).get_context_data()
    
    if self.object.tags.exists():
      tags_str_list = list()
      
      for t in self.object.tags.all():
        tags_str_list.append(t.name)
        
      context['tags_str_default'] = '; '.join(tags_str_list)
      
    return context
  
  def form_valid(self, form):
    response = super(BookmarkUpdate, self).form_valid(form)
    self.object.tags.clear()
    tags_str = self.request.POST.get('tags_str')
    
    if tags_str:
      tags_str = tags_str.strip()
      tags_str = tags_str.replace(',', ';')
      tags_list = tags_str.split(';')
      
      for t in tags_list:
        t = t.strip()
        tag, is_tag_created = Tag.objects.get_or_create(name=t)
        
        if is_tag_created:
          tag.slug = slugify(t, allow_unicode=True)
          tag.save()
        self.object.tags.add(tag)
    
    return response
  
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated and request.user == self.get_object().author:
      return super(BookmarkUpdate, self).dispatch(request, *args, **kwargs)
    else:
      raise PermissionDenied
