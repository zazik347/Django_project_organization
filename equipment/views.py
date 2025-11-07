import logging
from datetime import date

from django.db.models import Q
from django.shortcuts import render
from .models import Equipment, EquipmentAssignment

logger = logging.getLogger(__name__)

def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'equipment_list.html', {
        'equipment': equipment
    })

def equipment_distribution(request):

    # Дата по умолчанию — сегодня
    target_date_str = request.GET.get('date', date.today().isoformat())

    # Проверяем, что target_date_str — это строка
    if not isinstance(target_date_str, str):
        target_date_str = date.today().isoformat()

    try:
        target_date = date.fromisoformat(target_date_str.strip())
    except (ValueError, TypeError):
        target_date = date.today()

    # Фильтруем распределения, которые были активны к указанной дате
    active_assignments = EquipmentAssignment.objects.filter(
        assigned_date__lte=target_date
    )

    return render(request, 'distribution.html', {
        'target_date': target_date,
        'active_assignments': active_assignments,
    })



def equipment_list_by_period(request):
    # # Устанавливаем значения по умолчанию
    # start_date = date.today()
    # end_date = date.today()
    # Получаем даты из GET-параметров
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    if not start_date_str:
        start_date_str = date.today().isoformat()
    if not end_date_str:
        end_date_str = date.today().isoformat()

    # Проверяем и парсим start_date
    if isinstance(start_date_str, str) and start_date_str.strip():
        try:
            start_date = date.fromisoformat(start_date_str.strip())
        except ValueError:
          pass # Если формат неверный — оставляем сегодняшнюю дату
    else:
        start_date = date.today()

    # Проверяем и парсим end_date
    if isinstance(end_date_str, str) and end_date_str.strip():
        try:
            end_date = date.fromisoformat(end_date_str.strip())
        except ValueError:
         pass # Если формат неверный — оставляем сегодняшнюю дату
    else:
        end_date = date.today()
        # Формируем запрос
    query = Q(assigned_date__lte=end_date) & (Q(returned_date__isnull=True) | Q(returned_date__gte=start_date))


    active_assignments = EquipmentAssignment.objects.filter(query)

    return render(request, 'list_by_period.html', {
        'active_assignments': active_assignments,
        'start_date': start_date,
        'end_date': end_date,
    })

