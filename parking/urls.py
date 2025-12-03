from django.urls import path
from . import views

app_name = 'parking'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Vehículos
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/assign/', views.assign_vehicle, name='assign_vehicle'),
    
    # Reservas
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/normal/new/', views.normal_reservation, name='normal_reservation'),
    path('reservations/quick/new/', views.quick_reservation, name='quick_reservation'),
    path('reservations/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    # Asignaciones y Checkout
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/<int:pk>/checkout/', views.checkout, name='checkout'),
    path('assignments/<int:pk>/receipt/', views.print_receipt, name='print_receipt'),
    
    # Configuración
    path('configuration/spaces/', views.space_configuration, name='space_configuration'),
]
