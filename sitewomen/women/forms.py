from django import forms
from .models import Category, Husband
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

class AddPostForm(forms.Form):
  title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}),
                          error_messages={
                            'required': 'Без заголовка никак'
                          })
  content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), label="Контент")
  is_published = forms.BooleanField(label="Статус", initial=True)
  cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
  husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", required=False, label="Муж")

  def clean_title(self):
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
    title = self.cleaned_data.get('title', None)
    if not (set(title) <= set(ALLOWED_CHARS)):
      raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")