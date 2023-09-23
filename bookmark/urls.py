from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookmarkList.as_view()),
    path('<int:pk>/', views.BookmarkDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),
    path('create_bookmark/', views.BookmarkCreate.as_view()),
    path('update_bookmark/<int:pk>/', views.BookmarkUpdate.as_view()),
]

