from django.shortcuts import render, get_object_or_404
from .models import Department


def department_list(request):
    """Показывает список всех отделов"""
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    print(department)
    # employees = department.employee_set.all()  # Все сотрудники этого отдела
    return render(request, 'department_detail.html', {'department': department})

