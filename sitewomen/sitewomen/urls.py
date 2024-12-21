from django.contrib import admin
from django.urls import path, include
from women import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
]

# добавляет обработчик на страницу, который при ошибке 404 отрабатывает функцию page_not_found
handler404 = views.page_not_found

'''
Обработчики исключений работают только тогда, когда DEBUG=False
Виды обработчиков исключений:
* handler400 - если невозможно обработать запрос
* handler403 - доступ запрещен
* handler404 - страница не найдена
* handler500 - внутренняя ошибка сервера
'''
