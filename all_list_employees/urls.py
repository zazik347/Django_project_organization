from django.urls import path
from . import views

app_name = 'all_list_employees'

urlpatterns = [
    path('all/', views.staff_list, name='all_list'),
]
