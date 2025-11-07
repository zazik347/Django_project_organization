from django.urls import path
from . import views

app_name = 'constractors'

urlpatterns = [
    # path('constract_list/', views.design_department_list, name='constract_department_list'),
    path('constract_detail/', views.constract_department_detail, name='constract_department_detail'),
    path('engineer_constract/<int:pk>/', views.engineer_constract_detail, name='engineer_constract_detail'),
    path('edit_constractor/<int:pk>/', views.engineer_constract_update, name='engineer_constract_update'),
]
