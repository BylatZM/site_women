from django.apps import AppConfig

class WomenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
    verbose_name = "Женщины мира" # изменяет заголовок текущего раздела приложения women
