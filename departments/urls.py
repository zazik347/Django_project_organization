from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('department_list/', views.department_list, name='department_list'),
    path('department/<int:pk>/', views.department_detail, name='department_detail'),
]
