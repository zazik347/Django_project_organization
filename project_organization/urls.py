"""
URL configuration for project_organization project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path, include
from django.views.static import serve
from employees.views import get_project_dates

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page.urls', namespace='main_page')),
    path('', include('user.urls', namespace='user')),
    path('', include('user_profile.urls', namespace='user_profile')),
    path('', include('contracts.urls', namespace='contracts')),
    path('', include('departments.urls', namespace='departments')),
    path('', include('employees.urls', namespace='employees')),
    path('', include('equipment.urls', namespace='equipment')),
    path('', include('projects.urls', namespace='projects')),
    path('', include('subcontractors.urls', namespace='subcontractors')),
    path('', include('avtomatizations.urls', namespace='avtomatization')),
    path('', include('all_list_employees.urls', namespace='all_list_employees')),
    path('', include('constructors.urls', namespace='constractors')),
]

# Добавляем маршрут для медиафайлов (только в режиме разработки)
if settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]


admin.site.site_header = 'Панель администратора'
admin.site.index_title = 'Зарегистрированные пользователи'
