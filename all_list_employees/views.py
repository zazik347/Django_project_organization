from django.shortcuts import render
# from constructors.models import Constructor
from avtomatizations.models import AutomationEngineer


def staff_list(request):
    # Получаем всех сотрудников из обоих отделов
    # constructor_staff = Constructor.objects.all()
    automation_staff = AutomationEngineer.objects.all()

    # Объединяем их в один список
    all_staff = []
    for staff in automation_staff:
        all_staff.append({
            'full_name': staff.full_name,
            'department': 'Автоматизация',
            'role': staff.role.name if staff.role else 'Не указано',
        })

    return render(request, 'common/staff_list.html', {'all_staff': all_staff})
