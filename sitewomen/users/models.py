from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография пользователя")
  date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")

'''
В django есть возможность назначить пользователю группу прав, для этого нужно
1) Через панель администрации перейти во вкладку Группы
2) Нажать на создать группу
3) Дать название группе
4) Выбрать список нужных прав пользователя
5) Перейти в редактирование пользователя
6) В поле группы, выставить нужные права для пользователя и сохранить

Чтобы задать конкретные права для пользователя нужно в редактировании пользователя в переменной "права пользователя"
выставить нужные права для пользователя и сохранить

Пользователь с пометкой is_superuser имеет все права по умолчанию

Можно назначать группы прав пользователю через команды:
user = Women.objects.get(pk=1)
user.groups.set([group_list]) - назначить список груп прав
user.groups.add(group, group) - добавить группу прав
user.groups.remove(group, group) - удалить группу прав
user.groups.clear() - очистить все группы прав
user.groups.all() - позволяет просмотреть все группы прав пользователя

Можно назначать конкретные права пользователю через команды:
user = Women.objects.get(pk=1)
user.user_permissions.set([permission_list]) - назначить список прав
user.user_permissions.add(permission, permission) - добавить права
user.user_permissions.add(1) - добавит право под индексом 1 для пользователя
user.user_permissions.remove(permission, permission) - удалить права
user.user_permissions.clear() - очистить все права
user.user_permissions.all() - позволяет просмотреть все права пользователя

Есть дополнительный метод, такой как has_perm:
user = Women.objects.get(pk=1)
user.has_perm('women.add_women') - проверяет есть ли у пользователя право women.add_women

группу прав можно получить из класса
from django.contrib.auth.models import Permission
p = Permission.objects.get(codename='add_category')
print(p)
>> <Permission: women | Категория | Can add Категория>
user.user_permissions.add(p) - можем назначить пользователю право, которое заключено в экземпляре p класса Permission

from django.contrib.auth.models import Group

g = Group.objects.get(name='moderator')
user.groups.add(g) - назначаем пользователю группы прав
user.groups.add(1) - назначить пользователю группу прав под id 1

чтобы сформировать новое разрешение и добавить ее в список к другим можно так:
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
content_type = ContentType.objects.get_for_model(User)
permissions = Permission.objects.create(codename="social_auth", name="Social Auth", content_type=content_type)
'''