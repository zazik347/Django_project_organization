from django.urls import path
from . import views

app_name = 'subcontractors'
urlpatterns = [
    path('subcontractors/', views.subcontractor_list, name='subcontractor_list'),
]
