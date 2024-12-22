from django.db import models

class Women(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField(blank=True)
  time_create = models.DateTimeField(auto_now_add=True)
  time_update = models.DateTimeField(auto_now=True)
  is_published = models.BooleanField(default=True)

'''
По умолчанию все запросы к базе данных являются ленивыми
--------------------------------------------------------
Women(title="Анджелина Джоли", content="Биография Анджелины Джоли") - создает лишь экземпляр модели, но не добавляет его базу данных
--------------------------------------------------------
w = Women(title="Анджелина Джоли", content="Биография Анджелины Джоли") - создаем экземпляр, присваиваем переменной w
w.save() - сохраняем экземпляр в базе данных
'''