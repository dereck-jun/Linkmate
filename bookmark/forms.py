from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Bookmark, Tag

class TagChoiceField(forms.ModelMultipleChoiceField):
  def label_from_instance(self, obj):
    return obj.name


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
  
  
class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', "email", 'password1', 'password2']
  
  
  