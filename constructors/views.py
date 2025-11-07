from django.shortcuts import render, redirect

from django.shortcuts import render, get_object_or_404

from constructors.forms import ConstractorForm
from constructors.models import ConstrDepartment, Constructor


def design_department_list(request):
    """Показывает список всех конструкторских отделов"""
    departments = ConstrDepartment.objects.all()
    return render(request, 'constract_department_list.html', {'departments': departments})


def constract_department_detail(request):
    """Показывает структуру конкретного конструкторского отдела"""
    department = Constructor.objects.all()
    department_descr = get_object_or_404(ConstrDepartment)
    return render(request, 'constract_department_detail.html', {'department': department,
        'department_descr': department_descr})

def engineer_constract_detail(request, pk):
    worker = get_object_or_404(Constructor, pk=pk)
    return render(request, 'constract_engineer_detail.html', {
        'worker': worker
    })


def engineer_constract_update(request, pk):
    engineer = get_object_or_404(Constructor, pk=pk)
    if request.method == 'POST':
        form = ConstractorForm(request.POST, request.FILES, instance=engineer)
        # Проверяем, был ли установлен чекбокс
        clear_photo = request.POST.get('clear_photo') == 'on'
        if clear_photo:
            engineer.photo.delete(save=False)  # Удаляем фото из модели
            form.instance.photo = None  # Обнуляем поле формы
        if form.is_valid():
            form.save()
            return redirect('constractors:engineer_constract_detail', pk=engineer.pk)
    else:
        form = ConstractorForm(instance=engineer)

    return render(request, 'constract_engineer_form.html', {'form': form, 'engineer': engineer})
