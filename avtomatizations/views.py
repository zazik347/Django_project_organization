from django.db.models.functions import datetime
from django.shortcuts import render, get_object_or_404, redirect

from departments.models import Department
from .forms import EngineerForm
from .models import AutomationEngineer

from django.shortcuts import render, get_object_or_404
from .models import AutomationDepartment

def automation_department_list(request):
    pass
    """Показывает список всех отделов автоматизации"""
    departments = AutomationDepartment.objects.all()
    return render(request, 'avtomatiz_list.html', {'departments': departments})


def automation_department_detail(request):
    """Показывает структуру конкретного отдела автоматизации"""
    department = AutomationEngineer.objects.all()
    department_description = get_object_or_404(AutomationDepartment)
    return render(request, 'avtomatiz_detail.html', {'department': department,
                    'department_description': department_description})


def engineer_detail(request, pk):
    worker = get_object_or_404(AutomationEngineer, pk=pk)
    return render(request, 'engineer_detail.html', {
        'worker': worker
    })


def engineer_create(request):
    if request.method == 'POST':
        form = EngineerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('engineer_list')
    else:
        form = EngineerForm()
    return render(request, 'engineer_form.html', {'form': form})

def engineer_update(request, pk):
    engineer = get_object_or_404(AutomationEngineer, pk=pk)
    if request.method == 'POST':
        form = EngineerForm(request.POST, request.FILES, instance=engineer)
        # Проверяем, был ли установлен чекбокс
        clear_photo = request.POST.get('clear_photo') == 'on'
        if clear_photo:
            engineer.photo.delete(save=False)  # Удаляем фото из модели
            form.instance.photo = None  # Обнуляем поле формы
        if form.is_valid():
            form.save()
            return redirect('avtomatization:engineer_detail', pk=engineer.pk)
    else:
        form = EngineerForm(instance=engineer)

    return render(request, 'engineer_form.html', {'form': form, 'engineer': engineer})
