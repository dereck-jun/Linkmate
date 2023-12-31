from django.urls import path
from . import views
from .views import custom_login_view

urlpatterns = [
    # 다른 URL 패턴들
    path('login/', custom_login_view, name='login'),
]


urlpatterns = [
    path('', views.BookmarkList.as_view(), name='bookmark_list'),
    path('<int:pk>/', views.BookmarkDetail.as_view()),
    path('update_bookmark/<int:pk>/', views.BookmarkUpdate.as_view(), name='update_bookmark'),
    path('delete_bookmark/<int:pk>/', views.BookmarkDelete.as_view(), name='delete_bookmark'),
    path('tag/<str:slug>/', views.tag_page),
    path('create_bookmark/', views.BookmarkCreate.as_view()),
    path('search/<str:q>/', views.BookmarkSearch.as_view(), name='bookmark_search'),
    path('manage_tags/', views.ManageTags.as_view(), name='manage_tags'),
    path('tags/create/', views.TagCreate.as_view(), name='tag_create'),
    path('tags/detail/<str:slug>/', views.TagDetail.as_view(), name='tag_detail'),
    path('tags/delete/<str:slug>/', views.TagDelete.as_view(), name='tag_delete'),
    path('account/logout/', views.logout_page, name='logout'),
    path('account/login/', views.custom_login_view, name='login'),
    path('account/register/', views.register_page, name='register'),


]

