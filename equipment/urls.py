from django.urls import path
from . import views
app_name = 'equipment'

urlpatterns = [
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/distribution/', views.equipment_distribution, name='equipment_distribution'),
    path('equipment/list-by-period/', views.equipment_list_by_period, name='equipment_list_by_period'),
    path('issue/', views.issue_equipment, name='issue_equipment'),
    path('issued/', views.equipment_issued_list, name='issued_list')
]
