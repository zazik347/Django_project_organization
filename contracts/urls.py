from django.urls import path
from . import views

app_name = "contracts"

urlpatterns = [
    # path('contract/<int:pk>/projects/', views.contract_projects, name='contract_projects'),
    # path('contracts/', views.contract_list, name='contract_list'),
    # Получить проекты по договору
    path('contract/<int:contract_id>/projects/', views.projects_by_contract, name='projects_by_contract'),

    # Получить договор по проекту
    path('project/<int:project_id>/contract/', views.contracts_by_project, name='contracts_by_project'),
    # Получить данные о стоимости
    path('period-cost/', views.get_contracts_cost_in_period, name='period_cost'),
    path('project-costs/', views.project_costs, name='project_costs'),
]
