from datetime import date

from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404

from projects.models import Project
from .models import Contract

def get_contracts_cost_in_period(request):
    # Получаем даты из GET-параметров
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Фильтруем договоры, которые завершились в указанном периоде
    contracts = Contract.objects.filter(
        end_date__range=[start_date, end_date]
    )

    # Считаем общую стоимость
    total_cost = contracts.aggregate(Sum('total_cost'))['total_cost__sum'] or 0

    return render(request, 'period_cost.html', {
        'start_date': start_date,
        'end_date': end_date,
        'total_cost': total_cost,
        'contracts': contracts,
    })

def project_costs(request):
    today = date.today()
    # Все договоры, отсортированные по дате завершения (если есть)
    contracts = Contract.objects.all().order_by('end_date')

    # Разделение на выполненные и невыполненные
    completed_contracts = contracts.filter(end_date__lte=today).order_by('end_date')
    uncompleted_contracts = Contract.objects.filter(
        Q(end_date__gt=today) | Q(end_date__isnull=True)
    ).order_by('start_date')  # сортируем по дате начала
    return render(request, 'project_costs.html', {
        'completed_contracts': completed_contracts,
        'uncompleted_contracts': uncompleted_contracts,
    })

