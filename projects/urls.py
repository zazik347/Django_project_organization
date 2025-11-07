from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('project/<int:pk>/employees/', views.project_employees, name='project_employees'),
    path('project/<int:pk>/equipment/', views.project_equipment, name='project_equipment'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/export/', views.export_project_to_word, name='export_project'),
    # Список активных проектов
    path('active/', views.active_projects, name='active_projects'),
    # Список проектов по дате
    path('by-date/', views.projects_by_date, name='projects_by_date'),
    path('project/<int:project_id>/detail', views.search_project_detail, name='search_project_detail'),
    path('project-efficiency/', views.project_efficiency, name='project_efficiency'),
]
