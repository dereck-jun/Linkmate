from django.contrib import admin
from .models import Bookmark, Tag
# from .models import Bookmark, Category, Tag
# Register your models here.

admin.site.register(Bookmark)

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}



# admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
