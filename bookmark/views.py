from .models import Bookmark, Tag
from .forms import TagForm, BookmarkUpdateForm, BookmarkCreateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
# Create your views here.

class BookmarkCreate(CreateView):
  model = Bookmark
  form_class = BookmarkCreateForm
  success_url = '/bookmark/'
  
  def get_form_kwargs(self):
    kwargs = super(BookmarkCreate, self).get_form_kwargs()
    kwargs['user'] = self.request.user  # user 인자를 폼으로 전달
    return kwargs
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super(BookmarkCreate, self).form_valid(form)


class BookmarkList(ListView):
  model = Bookmark
  ordering = ['title']
  paginate_by = 5
  
  def get_queryset(self):
    # 로그인한 사용자의 북마크만 가져오도록 쿼리셋 수정
    if self.request.user.is_authenticated:
      return Bookmark.objects.filter(author=self.request.user).order_by('title')
    else:
      # 비로그인 사용자의 경우 빈 쿼리셋 반환
      return Bookmark.objects.none()
  
  def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data()
    context['tags'] = Tag.objects.all()
    
    if self.request.user.is_authenticated:
      # 로그인한 경우 카테고리 및 미분류 포스트 개수 계산
      context['no_tags_bookmark_count'] = Bookmark.objects.filter(
        author=self.request.user, tags=None
      ).count()
    else:
      # 비로그인 사용자의 경우 미분류 포스트 개수 계산 불가능
      context['no_tags_bookmark_count'] = None
    
    return context

def tag_page(request, slug):
  tag = Tag.objects.get(slug=slug)
  bookmark_list = tag.bookmark_set.filter(author=request.user)
  
  return render(request, 'bookmark/bookmark_list.html', {
    'bookmark_list': bookmark_list,
    'tag': tag,
    })

  
class BookmarkDetail(DetailView):
  model = Bookmark
  
  def get_context_data(self, **kwargs):
    context = super(BookmarkDetail, self).get_context_data()
    context['tags'] = Tag.objects.all()
    context['no_tags_bookmark_count'] = Bookmark.objects.filter(tags=None).count()
    
    return context
  

class BookmarkUpdate(UpdateView):
  model = Bookmark
  form_class = BookmarkUpdateForm
  
  def get_form_kwargs(self):
    kwargs = super(BookmarkUpdate, self).get_form_kwargs()
    kwargs['user'] = self.request.user  # user 인자를 폼으로 전달
    return kwargs
  
  def dispatch(self, request, *args, **kwargs):
    bookmark = get_object_or_404(Bookmark, pk=kwargs['pk'])
    if request.user.is_authenticated and request.user == bookmark.author:
      return super(BookmarkUpdate, self).dispatch(request, *args, **kwargs)
    else:
      raise PermissionDenied


  
class BookmarkDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Bookmark
  success_url = '/bookmark/'  # 북마크가 성공적으로 삭제된 후 리다이렉트할 URL 설정
  template_name = 'bookmark/bookmark_delete.html'
  
  def test_func(self):
    bookmark = self.get_object()
    return self.request.user == bookmark.author

class BookmarkSearch(BookmarkList):
  paginate_by = 5
  
  def get_queryset(self):
    q = self.kwargs['q']
    bookmark_list = Bookmark.objects.filter(
      Q(title__contains=q) | Q(tags__name__contains=q),
      author=self.request.user
    ).distinct()
    return bookmark_list
  
  def get_context_data(self, **kwargs):
    context = super(BookmarkSearch, self).get_context_data()
    q = self.kwargs['q']
    context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
    
    return context
  
class ManageTags(ListView):
  model = Tag
  context_object_name = 'tags'
  template_name = 'bookmark/manage_tags.html'
  
  def get(self, request, *args, **kwargs):
    user_tags = Tag.objects.filter(author=request.user)
    
    return render(request, self.template_name, {'user_tags': user_tags})
  
  
class TagCreate(CreateView):
  model = Tag
  form_class = TagForm
  template_name = 'bookmark/tag_form.html'
  success_url = '/bookmark/manage_tags/'
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    
    return super().form_valid(form)
  
  
class TagDetail(DetailView):
  model = Tag
  
  def get_context_data(self, **kwargs):
    context = super(TagDetail, self).get_context_data(**kwargs)
    tag = get_object_or_404(Tag, slug=self.kwargs['slug'], author=self.request.user)
    # 로그인한 사용자의 북마크에서만 해당 태그와 연결된 북마크 가져오기
    context['bookmarks_with_tag'] = Bookmark.objects.filter(tags=tag, author=self.request.user)
    return context
  
  
class TagDelete(DeleteView):
  model = Tag
  template_name = 'bookmark/tag_delete.html'
  success_url = '/bookmark/manage_tags/'
  
