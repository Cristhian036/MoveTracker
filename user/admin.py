from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para User con campos dni y phone"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'dni', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'phone')
    ordering = ('username',)
    
    # Añadir dni y phone a los fieldsets del formulario de edición
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('dni', 'phone')}),
    )
    
    # Añadir dni y phone al formulario de creación
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('dni', 'phone')}),
    )
