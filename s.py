import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placesRemember.settings')  # Укажите путь к файлу settings.py вашего проекта
django.setup()

from django.contrib.auth.models import User

# Проверяем, существует ли уже суперпользователь
if not User.objects.filter(username='admin').exists():
    # Создаем суперпользователя
    User.objects.create_superuser('root', 'chikovm@bk.ru', 'root')
    print('Superuser created successfully.')
else:
    print('Superuser already exists.')