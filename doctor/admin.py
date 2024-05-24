from django.contrib import admin
from .models import Department,Doctor,AvailabilityTime,DoctorAvailability


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'specialization', 'fees')
    search_fields = ('name', 'location', 'specialization', 'fees')
    list_filter = ('name', 'location', 'specialization', 'fees')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('department', 'user')
    search_fields = ('department', 'user')
    list_filter = ('department', 'user')

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(AvailabilityTime)
admin.site.register(DoctorAvailability)
