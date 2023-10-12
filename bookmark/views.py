from .models import Bookmark, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q
# Create your views here.

class BookmarkCreate(LoginRequiredMixin, CreateView):
  model = Bookmark
  # fields = ['title', 'url', 'head_image', 'category']
  fields = ['title', 'url', 'head_image', 'tags']
  
  def form_valid(self, form):
    # 현재 로그인한 사용자를 북마크의 저자로 설정
    form.instance.author = self.request.user
    
    # 기본 form_valid 메서드 실행
    response = super().form_valid(form)
    
    # 태그 입력 처리
    tags_str = self.request.POST.get('tags_str')
    if tags_str:
      tags_str = tags_str.strip()  # 공백 제거
      tags_list = tags_str.split()  # 공백을 기준으로 태그 목록 분리
      
      for t in tags_list:
        t = t.strip()  # 각 태그의 양쪽 공백 제거
        tag, is_tag_created = Tag.objects.get_or_create(name=t)
        if is_tag_created:
          tag.slug = slugify(t, allow_unicode=True)  # 태그 이름을 기반으로 슬러그 생성
          tag.save()
        self.object.tags.add(tag)  # 북마크와 태그 연결
    
    return response


class BookmarkList(ListView):
  model = Bookmark
  ordering = "title"
  paginate_by = 5
  
  def get_queryset(self):
    # 로그인한 사용자의 북마크만 가져오도록 쿼리셋 수정
    if self.request.user.is_authenticated:
      return Bookmark.objects.filter(author=self.request.user)
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
  
# def category_page(request, slug):
#   if slug == 'no_category':
#     category = '미분류'
#     bookmark_list = Bookmark.objects.filter(category=None)
#   else:
#     category = Category.objects.get(slug=slug)
#     bookmark_list = Bookmark.objects.filter(category=category)
#
#   return render(request, 'bookmark/bookmark_list.html', {
#     'bookmark_list': bookmark_list,
#     'categories': Category.objects.all(),
#     'no_category_bookmark_count': Bookmark.objects.filter(category=None).count(),
#     'category': category,
#   })

def tag_page(request, slug):
  tag = Tag.objects.get(slug=slug)
  bookmark_list = tag.bookmark_set.all()
  
  return render(request, 'bookmark/bookmark_list.html', {
    'bookmark_list': bookmark_list,
    'tag': tag,
    # 'categories': Category.objects.all(),
    'no_tags_bookmark_count': Bookmark.objects.filter(tags=None).count(),
    })

  
class BookmarkDetail(DetailView):
  model = Bookmark
  
  def get_context_data(self, **kwargs):
    context = super(BookmarkDetail, self).get_context_data()
    context['tags'] = Tag.objects.all()
    context['no_tags_bookmark_count'] = Bookmark.objects.filter(tags=None).count()
    
    return context
  
  
class BookmarkUpdate(LoginRequiredMixin, UpdateView):
  model = Bookmark
  # fields = ['title', 'url', 'head_image', 'category', 'tags']
  fields = ['title', 'url', 'head_image', 'tags']
  template_name = 'bookmark/bookmark_update_form.html'
  
  def dispatch(self, request, *args, **kwargs):
    bookmark = get_object_or_404(Bookmark, pk=kwargs['pk'])
    if request.user.is_authenticated and request.user == bookmark.author:
      return super(BookmarkUpdate, self).dispatch(request, *args, **kwargs)
    else:
      raise PermissionDenied
  
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
  
class BookmarkDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Bookmark
  success_url = '/success/url/'  # 북마크가 성공적으로 삭제된 후 리다이렉트할 URL 설정
  
  def test_func(self):
    bookmark = self.get_object()
    return self.request.user == bookmark.author

class BookmarkSearch(BookmarkList):
  paginate_by = None
  
  def get_queryset(self):
    q = self.kwargs['q']
    bookmark_list = Bookmark.objects.filter(
      Q(title__contains=q) | Q(tags__name__contains=q)
    ).distinct()
    return bookmark_list
  
  def get_context_data(self, **kwargs):
    context = super(BookmarkSearch, self).get_context_data()
    q = self.kwargs['q']
    context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
    
    return context
  