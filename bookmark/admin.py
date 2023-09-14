from django.contrib import admin
from .models import Bookmark, Category
# Register your models here.

admin.site.register(Bookmark)

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}
  
admin.site.register(Category, CategoryAdmin)