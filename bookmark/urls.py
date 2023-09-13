from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.BookmarkList.as_view()),
    path('<int:pk>/', views.BookmarkDetail.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)