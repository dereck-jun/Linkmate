from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookmarkList.as_view()),
    path('<int:pk>/', views.BookmarkDetail.as_view()),
    path('update_bookmark/<int:pk>/', views.BookmarkUpdate.as_view(), name='update_bookmark'),
    path('delete_bookmark/<int:pk>/', views.BookmarkDelete.as_view(), name='delete_bookmark'),
    path('tag/<str:slug>/', views.tag_page),
    path('create_bookmark/', views.BookmarkCreate.as_view()),
    path('search/<str:q>/', views.BookmarkSearch.as_view(), name='bookmark_search'),
]

