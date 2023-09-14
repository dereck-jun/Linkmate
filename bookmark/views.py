from .models import Bookmark, Category
from django.views.generic import ListView, DetailView
from django.shortcuts import render
# Create your views here.
class BookmarkList(ListView):
  model = Bookmark
  ordering = "title"
  
  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(BookmarkList, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Bookmark.objects.filter(category=None).count()
    
    return context
  
  
class BookmarkDetail(DetailView):
  model = Bookmark