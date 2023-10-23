from django import forms
from .models import Bookmark, Tag


class BookmarkForm(forms.ModelForm):
  # class Meta:
  #   model = Bookmark
  #   fields = ['title', 'url', 'head_image', 'tags']
  #   widgets = {
  #     'tags': forms.SelectMultiple(attrs={'class': 'select2-tags'}),  # SelectMultiple로 변경
  #   }
  #
  # def __init__(self, user, *args, **kwargs):
  #   super(BookmarkForm, self).__init__(*args, **kwargs)
  #   self.fields['tags'].queryset = Tag.objects.filter(author=user)
  class Meta:
    model = Bookmark
    fields = ['title', 'url', 'head_image', 'tags']
    widgets = {
      'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
    }
  
  def __init__(self, user, *args, **kwargs):
    super(BookmarkForm, self).__init__(*args, **kwargs)
    self.fields['tags'].queryset = Tag.objects.filter(author=user)


class TagForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ['name']

