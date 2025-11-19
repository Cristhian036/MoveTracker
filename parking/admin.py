from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    ParkingConfiguration,
    VehicleTariff,
    Vehicle,
    ParkingFloor,
    ParkingSpace,
    ParkingAssignment,
    ParkingReservation
)


@admin.register(ParkingConfiguration)
class ParkingConfigurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_floors', 'spaces_per_floor', 'total_capacity', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'total_capacity']
    
    fieldsets = (
        ('Configuración del Estacionamiento', {
            'fields': ('total_floors', 'spaces_per_floor', 'total_capacity')
        }),
        ('Estado', {
            'fields': ('is_active', 'created_by')
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(VehicleTariff)
class VehicleTariffAdmin(admin.ModelAdmin):
    list_display = ['vehicle_type_display', 'rate_per_hour', 'is_active', 'updated_at']
    list_filter = ['is_active', 'vehicle_type']
    search_fields = ['vehicle_type']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Tipo de Vehículo', {
            'fields': ('vehicle_type',)
        }),
        ('Tarifas', {
            'fields': ('rate_per_hour',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def vehicle_type_display(self, obj):
        return obj.get_vehicle_type_display()
    vehicle_type_display.short_description = 'Tipo de Vehículo'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'vehicle_type_badge', 'brand', 'model', 'year', 'owner_link', 'is_active', 'created_at']
    list_filter = ['is_active', 'vehicle_type', 'created_at', 'brand']
    search_fields = ['license_plate', 'brand', 'model', 'owner__username', 'owner__email']
    readonly_fields = ['created_at', 'updated_at', 'registered_by']
    autocomplete_fields = ['owner']
    
    fieldsets = (
        ('Información del Vehículo', {
            'fields': ('vehicle_type', 'brand', 'model', 'year', 'color', 'license_plate')
        }),
        ('Propietario', {
            'fields': ('owner',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Registro', {
            'fields': ('registered_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.registered_by = request.user
        super().save_model(request, obj, form, change)

    def vehicle_type_badge(self, obj):
        colors = {
            'CAR': 'blue',
            'TRUCK': 'orange',
            'MOTORCYCLE': 'green'
        }
        color = colors.get(obj.vehicle_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_vehicle_type_display()
        )
    vehicle_type_badge.short_description = 'Tipo'

    def owner_link(self, obj):
        if obj.owner:
            url = reverse('admin:user_user_change', args=[obj.owner.id])
            return format_html('<a href="{}">{}</a>', url, obj.owner.username)
        return '-'
    owner_link.short_description = 'Propietario'


@admin.register(ParkingFloor)
class ParkingFloorAdmin(admin.ModelAdmin):
    list_display = ['floor_name', 'floor_number', 'configuration', 'spaces_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'configuration', 'created_at']
    search_fields = ['floor_name', 'floor_number']
    readonly_fields = ['created_at', 'spaces_count']
    
    def spaces_count(self, obj):
        return obj.spaces.count()
    spaces_count.short_description = 'Espacios'


@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ['full_code', 'floor', 'space_number', 'status_badge', 'is_active', 'updated_at']
    list_filter = ['status', 'is_active', 'floor__floor_number', 'updated_at']
    search_fields = ['space_number', 'floor__floor_name']
    readonly_fields = ['created_at', 'updated_at', 'full_code']
    
    fieldsets = (
        ('Ubicación', {
            'fields': ('floor', 'space_number', 'full_code')
        }),
        ('Estado', {
            'fields': ('status', 'is_active')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'AVAILABLE': 'green',
            'OCCUPIED': 'red',
            'RESERVED': 'orange',
            'MAINTENANCE': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'


@admin.register(ParkingAssignment)
class ParkingAssignmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle_info', 'parking_space', 'status_badge', 'entry_time', 'exit_time', 'total_cost', 'assigned_by']
    list_filter = ['status', 'entry_time', 'exit_time', 'parking_space__floor__floor_number']
    search_fields = ['vehicle__license_plate', 'vehicle__owner__username', 'parking_space__space_number']
    readonly_fields = ['created_at', 'updated_at', 'entry_time', 'total_cost']
    autocomplete_fields = ['vehicle', 'parking_space', 'assigned_by', 'completed_by']
    date_hierarchy = 'entry_time'
    
    fieldsets = (
        ('Asignación', {
            'fields': ('vehicle', 'parking_space', 'status')
        }),
        ('Tiempos', {
            'fields': ('entry_time', 'planned_exit_time', 'exit_time')
        }),
        ('Costo', {
            'fields': ('total_cost',)
        }),
        ('Observaciones', {
            'fields': ('notes',)
        }),
        ('Responsables', {
            'fields': ('assigned_by', 'completed_by')
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)

    def vehicle_info(self, obj):
        return f"{obj.vehicle.license_plate} ({obj.vehicle.get_vehicle_type_display()})"
    vehicle_info.short_description = 'Vehículo'

    def status_badge(self, obj):
        colors = {
            'ACTIVE': 'green',
            'COMPLETED': 'blue',
            'CANCELLED': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'


@admin.register(ParkingReservation)
class ParkingReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation_type_badge', 'customer_display', 'vehicle_display', 'parking_space', 'status_badge', 'reservation_date', 'duration_minutes', 'created_at']
    list_filter = ['status', 'is_quick_reservation', 'reservation_date', 'created_at', 'vehicle_type_temp']
    search_fields = ['user__username', 'vehicle__license_plate', 'customer_name', 'customer_phone', 'vehicle_plate', 'parking_space__space_number']
    readonly_fields = ['created_at', 'updated_at', 'customer_info', 'vehicle_info']
    autocomplete_fields = ['user', 'vehicle', 'parking_space', 'created_by']
    date_hierarchy = 'reservation_date'
    
    fieldsets = (
        ('Tipo de Reserva', {
            'fields': ('is_quick_reservation',),
            'description': 'Marque esta opción para crear una reserva rápida/manual sin usuario registrado'
        }),
        ('Usuario Registrado (Reserva Normal)', {
            'fields': ('user', 'vehicle'),
            'classes': ('collapse',),
            'description': 'Solo para reservas de usuarios registrados'
        }),
        ('Datos del Cliente (Reserva Rápida)', {
            'fields': ('customer_name', 'customer_phone', 'customer_email'),
            'classes': ('collapse',),
            'description': 'Para reservas rápidas sin usuario registrado'
        }),
        ('Datos del Vehículo (Reserva Rápida)', {
            'fields': ('vehicle_plate', 'vehicle_type_temp'),
            'classes': ('collapse',),
            'description': 'Para reservas rápidas sin vehículo registrado'
        }),
        ('Asignación de Espacio', {
            'fields': ('parking_space', 'status')
        }),
        ('Fecha y Duración', {
            'fields': ('reservation_date', 'duration_minutes')
        }),
        ('Información Adicional', {
            'fields': ('notes', 'created_by')
        }),
        ('Resumen', {
            'fields': ('customer_info', 'vehicle_info'),
            'classes': ('collapse',),
            'description': 'Resumen de la información del cliente y vehículo'
        }),
        ('Fechas del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def reservation_type_badge(self, obj):
        if obj.is_quick_reservation:
            return format_html(
                '<span style="background-color: purple; color: white; padding: 3px 10px; border-radius: 3px;">⚡ RÁPIDA</span>'
            )
        else:
            return format_html(
                '<span style="background-color: blue; color: white; padding: 3px 10px; border-radius: 3px;">👤 NORMAL</span>'
            )
    reservation_type_badge.short_description = 'Tipo'

    def customer_display(self, obj):
        if obj.is_quick_reservation:
            return obj.customer_name or obj.customer_phone or 'Sin datos'
        else:
            return obj.user.username if obj.user else 'Sin usuario'
    customer_display.short_description = 'Cliente'

    def vehicle_display(self, obj):
        if obj.is_quick_reservation:
            return obj.vehicle_plate or 'Sin placa'
        else:
            return obj.vehicle.license_plate if obj.vehicle else 'Sin vehículo'
    vehicle_display.short_description = 'Vehículo'

    def status_badge(self, obj):
        colors = {
            'PENDING': 'orange',
            'CONFIRMED': 'green',
            'CANCELLED': 'red',
            'COMPLETED': 'blue'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
