from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from women import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls'), name="users"),
    path('__debug__/', include("debug_toolbar.urls")),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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

admin.site.site_header = "Панель администрирования" # изменяет самый верхний заголовок в панели администрирования (может принимать None, тогда значение будет по дефолту)

admin.site.index_title = "Известные женщины мира" # изменяет верхний заголовок в панели администрирования (может принимать None, тогда поле не будет отображаться)