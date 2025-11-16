import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_organization.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Создание суперпользователя (если ещё не существует)
username = 'admin'
email = 'admin@example.com'
password = 'admin123'  # Сменить потом!

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Суперпользователь "{username}" создан')
else:
    print(f'✅ Суперпользователь "{username}" уже существует')
