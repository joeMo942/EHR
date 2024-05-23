from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    list_display_links = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    filter_horizontal=()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'type', 'ssn', 'contact_no', 'birth_date', 'gender')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'type', 'ssn', 'contact_no', 'birth_date', 'gender', 'is_admin', 'is_staff', 'is_active', 'is_superadmin'),
    #     }),
    # )
    add_fieldsets=(
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'type', 'ssn', 'contact_no', 'birth_date', 'gender')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin')}),    )


admin.site.register(Account, AccountAdmin)