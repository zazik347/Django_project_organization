import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_organization.settings")
django.setup()

from employees.models import Employee
from projects.models import Project
from equipment.models import EquipmentAssignment
from datetime import datetime, date

def fix_date_format(model, field_name):
    for obj in model.objects.all():
        if getattr(obj, field_name) is not None:
            try:
                # Пытаемся преобразовать текущее значение в строку и обратно в date
                current_value = str(getattr(obj, field_name))
                parsed_date = date.fromisoformat(current_value)
                if parsed_date != getattr(obj, field_name):
                    setattr(obj, field_name, parsed_date)
                    obj.save()
            except (ValueError, TypeError):
                print(f"Ошибка при обработке {obj} - поле {field_name}")

# Запускаем для каждой модели
fix_date_format(Employee, 'start_date')
fix_date_format(Employee, 'birth_date')
fix_date_format(Project, 'start_date')
fix_date_format(Project, 'end_date')
fix_date_format(EquipmentAssignment, 'assigned_date')
fix_date_format(EquipmentAssignment, 'returned_date')

print("Обновление дат завершено.")
