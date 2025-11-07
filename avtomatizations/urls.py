from django.urls import path
from . import views

app_name = 'avtomatization'

urlpatterns = [
    path('avtomatiz_detail/', views.automation_department_detail, name='automation_department_detail'),
    path('avtomatiz_list/', views.automation_department_list, name='automation_department_list'),
    path('engineer/<int:pk>/', views.engineer_detail, name='engineer_detail'),
    path('edit/<int:pk>/', views.engineer_update, name='engineer_update'),
]
