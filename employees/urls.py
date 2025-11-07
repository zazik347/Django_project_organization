from django.urls import path
from . import views
from .views import get_project_dates

app_name = 'employees'

urlpatterns = [
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    # path('employee/<int:pk>/edit/', views.edit_employee, name='edit_employee'),
    path('employees/', views.employee_list, name='employee_list'),
    path('manager_list/', views.manager_list, name='manager_list'),
    path('add-project-employees/', views.add_project_employees, name='add_project_employees'),
    path('get-project-dates/', get_project_dates, name='get_project_dates'),
    path('bulk-create-assignments/', views.bulk_create_employee_assignments, name='bulk_create_assignments'),
]
