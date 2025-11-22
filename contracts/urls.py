from django.urls import path
from . import views

app_name = "contracts"

urlpatterns = [
    # Получить данные о стоимости
    path('period-cost/', views.get_contracts_cost_in_period, name='period_cost'),
    path('project-costs/', views.project_costs, name='project_costs'),
]
