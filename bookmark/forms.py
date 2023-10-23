from django import forms
from .models import Bookmark, Tag

class TagChoiceField(forms.ModelMultipleChoiceField):
  def label_from_instance(self, obj):
    return obj.name

# class BookmarkForm(forms.ModelForm):
#   tags = TagChoiceField(
#     queryset=Tag.objects.none(),
#     widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
#     required=False
#   )
#   class Meta:
#     model = Bookmark
#     fields = ['title', 'url', 'head_image', 'tags']
#
#   def __init__(self, user, *args, **kwargs):
#     super(BookmarkForm, self).__init__(*args, **kwargs)
#     self.fields['tags'].queryset = Tag.objects.filter(author=user)

class BookmarkCreateForm(forms.ModelForm):
  tags = forms.ModelMultipleChoiceField(
    queryset=Tag.objects.none(),
    widget=forms.CheckboxSelectMultiple,
    required=False
  )
  
  class Meta:
    model = Bookmark
    fields = ['title', 'url', 'head_image', 'tags']
  
  def __init__(self, user, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['tags'].queryset = Tag.objects.filter(author=user)


class BookmarkUpdateForm(forms.ModelForm):
  tags = forms.ModelMultipleChoiceField(
    queryset=Tag.objects.none(),
    widget=forms.CheckboxSelectMultiple,
    required=False
  )

  class Meta:
    model = Bookmark
    fields = ['title', 'url', 'head_image', 'tags']
  
  def __init__(self, user, *args, **kwargs):
    super(BookmarkUpdateForm, self).__init__(*args, **kwargs)
    # 현재 사용자가 만든 태그만 필드에 표시되도록 필터링
    self.fields['tags'].queryset = Tag.objects.filter(author=user)


class TagForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ['name']
  
  
  
  
  
  