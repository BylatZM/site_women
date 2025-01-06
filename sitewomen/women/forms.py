from django import forms
from .models import Category, Husband, Women
# from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

# класс валидатор, который можно использовать в списке атрибута validators у полей формы или модели
# @deconstructible
# class RussianValidator:
#   ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
#   code = 'russian'

#   def __init__(self, message=None):
#     self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

#   def __call__(self, value, *args, **kwds):
#     if not (set(value) <= set(self.ALLOWED_CHARS)):
#       raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.ModelForm):
  cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
  husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", required=False, label="Муж")

  class Meta:
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
    # позволяет задать стили оформления, а также формат поля
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input'}),
      'content': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'style': 'resize: none;'})
    }
    # позволяет изменить названия полей формы
    # labels = {
    #   'slug': 'URL'
    # }

  def clean_title(self):
    title = self.cleaned_data.get('title', '')
    if len(title) > 50:
      raise ValidationError("Длина превышает 50 символов")
    
    return title
  
class UploadFileForm(forms.Form):
  # file = forms.FileField(label="Файл") - возворяет загружать не только картинки, но и word, pdf и т.д файлы
  file = forms.ImageField(label="Файл")