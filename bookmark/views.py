from .models import Bookmark
from django.views.generic import ListView, DetailView

# Create your views here.
class BookmarkList(ListView):
  model = Bookmark
  ordering = "title"
  
class BookmarkDetail(DetailView):
  model = Bookmark