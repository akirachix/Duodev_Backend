from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from textilebale.models import TextileBale

class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ['-registration_date']
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('registration_date',)
    filter_horizontal = ()
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'registration_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
