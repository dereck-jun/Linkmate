from .models import Bookmark, Category, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
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
      return super(BookmarkCreate, self).form_valid(form)
    else:
      return redirect('/bookmark/')

class BookmarkList(ListView):
  model = Bookmark
  ordering = "title"
  
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
  
  