import json
from datetime import timedelta, date

from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from avtomatizations.models import AutomationEngineer, AutomationRole
from constructors.models import Constructor, ConstructorRole
from projects.models import Project
# from .forms import EmployeeForm
from .models import Employee, EmployeeAssignment


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {
        'employee': employee
    })
def employee_list(request):
    employees = Employee.objects.all()
    engineers = AutomationEngineer.objects.all()
    constructors = Constructor.objects.all()
    return render(request, 'employee_list.html', {'employees': employees,
                  'engineers': engineers,
                  'constructors': constructors})

def filtered_employee_list(request):
    # Получаем всех сотрудников
    employees = list(Employee.objects.all())


    # Объединяем
    all_employees = employees

    # Получаем фильтры
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')

    today = timezone.now().date()

    # Функция для расчёта возраста
    def calculate_age(birth_date):
        if not birth_date:
            return None
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )

    # Фильтруем в Python
    filtered_employees = []
    for emp in all_employees:
        age = calculate_age(emp.birth_date)  # Считаем возраст
        emp._age = age  # Сохраняем как временное поле (не трогаем @property)

        if age is None:
            continue

        # Проверяем фильтры
        if age_min and age < int(age_min):
            continue
        if age_max and age > int(age_max):
            continue

        filtered_employees.append(emp)

    # Сортируем по имени
    filtered_employees.sort(key=lambda x: x.full_name)

    return render(request, 'filter_list.html', {
        'employees': filtered_employees,
        'age_min': age_min,
        'age_max': age_max,
    })

def manager_list(request):
    # Получаем начальников из автоматизации
    automation_heads = AutomationEngineer.objects.filter(role__is_head=True)
    print(automation_heads)


    # Получаем начальников из конструкторского отдела
    constructor_heads = Constructor.objects.filter(role__is_head=True)

    return render(request, 'manager_list.html', {
        'automation_heads': automation_heads,
        'constructor_heads': constructor_heads,
    })

def get_project_dates(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id')
        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
                # Получаем сотрудников через ProjectEmployee и их full_name из Employee
                employees = []
                for pe in project.employees.all():
                    emp = pe.employee
                    employees.append({
                        'id': emp.id,
                        'full_name': emp.full_name  # теперь точно есть
                    })
                return JsonResponse({
                    'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
                    'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
                    'employees': employees
                })
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Project not found'}, status=404)
        else:
            return JsonResponse({'error': 'Missing project_id'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt  # Только если используешь без CSRF-токена (в админке можно)
@permission_required('employees.add_employeeassignment')
def add_project_employees(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('project_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            project = get_object_or_404(Project, pk=project_id)

            # Получаем всех сотрудников из new_employees_more
            employees = project.new_employees_more.all()

            created = []
            for employee in employees:
                # Проверим, нет ли уже такой записи
                obj, created_flag = EmployeeAssignment.objects.get_or_create(
                    employee=employee,
                    project=project,
                    defaults={
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )
                if created_flag:
                    created.append(employee.full_name)

            return JsonResponse({
                'status': 'success',
                'created': created,
                'count': len(created)
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
@permission_required('employees.add_employeeassignment')
def bulk_create_employee_assignments(request):
    if request.method == 'POST':
        try:
            # Если данные приходят как form-data
            project_id = request.POST.get('project_id')
            employee_id = request.POST.get('employee_id')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            obj, created = EmployeeAssignment.objects.get_or_create(
                employee_id=employee_id,
                project_id=project_id,
                defaults={'start_date': start_date, 'end_date': end_date}
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


