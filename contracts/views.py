from datetime import date

from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404

from projects.models import Project
from .models import Contract


def contract_cost_report(request):
    pass
    # from datetime import datetime
    # start_date = request.GET.get('start_date')
    # end_date = request.GET.get('end_date')
    #
    # if start_date and end_date:
    #     start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    #     end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    #     contracts = Contract.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
    # else:
    #     contracts = Contract.objects.all()
    #
    # total_cost = sum(contract.total_cost for contract in contracts)
    #
    # return render(request, 'report.html', {
    #     'contracts': contracts,
    #     'total_cost': total_cost
    # })


def projects_by_contract(request, contract_id):
    pass
    # # Получаем договор по ID
    # contract = get_object_or_404(Contract, id=contract_id)
    # # Получаем все проекты, связанные с этим договором
    # projects = contract.project_more
    #
    # return render(request, 'projects_by_contract.html', {
    #     'contract': contract,
    #     'projects': projects,
    # })


def contracts_by_project(request, project_id):
    pass
#     # Получаем проект по ID
#     project = get_object_or_404(Project, id=project_id)
#     # Получаем договор, к которому относится этот проект
#     contract = project.contract
#
#     return render(request, 'contracts_by_project.html', {
#         'project': project,
#         'contract': contract,
#     })

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

