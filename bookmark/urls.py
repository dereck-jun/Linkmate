from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookmarkList.as_view()),
    path('<int:pk>/', views.BookmarkDetail.as_view()),
]
