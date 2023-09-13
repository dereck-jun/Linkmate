from django.shortcuts import render
from .models import Bookmark
from django.views.generic import ListView

# Create your views here.
class BookmarkList(ListView):
  model = Bookmark
  ordering = "title"
  
def single_list_page(request, pk):
  bookmark = Bookmark.objects.get(pk=pk)
  
  return render(request, 'bookmark/single_list_page.html', {'bookmark': bookmark})