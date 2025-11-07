from django.contrib import admin
from django.urls import path
from django.shortcuts import render
# from constructors.models import Constructor
from avtomatizations.models import AutomationEngineer


class UnifiedStaffAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('all-staff/', self.admin_site.admin_view(self.all_staff_view), name='all-staff'),
        ]
        return custom_urls + urls
    def all_staff_view(self, request):
        # Получаем всех сотрудников из обоих моделей
        # constructor_staff = Constructor.objects.all()
        automation_staff = AutomationEngineer.objects.all()

        staff_list = []

        # for staff in constructor_staff:
        #     staff_list.append({
        #         'full_name': staff.full_name,
        #         'department': 'Конструкторы',
        #         'role': staff.role.name if staff.role else 'Не указано',
        #     })
        for staff in automation_staff:
            staff_list.append({
                'full_name': staff.full_name,
                'department': 'Автоматизация',
                'role': staff.role.name if staff.role else 'Не указано',
            })

        context = dict(
            self.admin_site.each_context(request),
            title="Все сотрудники",
            staff_list=staff_list,
        )

        return render(request, 'all_list.html', context)
