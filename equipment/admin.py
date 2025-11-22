from django.contrib import admin
from equipment.models import Equipment, EquipmentAssignment, EquipmentTransfer

# Register your models here.
admin.site.register(Equipment)
admin.site.register(EquipmentAssignment)

@admin.register(EquipmentTransfer)
class EquipmentTransferAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'from_department', 'to_department', 'transfer_date', 'responsible_person')
    list_filter = ('transfer_date', 'from_department', 'to_department')
    search_fields = ('equipment__name', 'responsible_person')
    readonly_fields = ('transfer_date',)
