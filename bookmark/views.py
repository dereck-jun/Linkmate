from django.shortcuts import render
from .models import Bookmark
# Create your views here.
def index(request):
  bookmarks = Bookmark.objects.all().order_by('title')
  
  return render(request, 'bookmark/index.html', {'bookmarks': bookmarks})

def single_list_page(request, pk):
  bookmark = Bookmark.objects.get(pk=pk)
  
  return render(request, 'bookmark/single_list_page.html', {'bookmark': bookmark})