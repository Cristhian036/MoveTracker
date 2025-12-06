from django.shortcuts import render, redirect
from django.contrib import messages

def csrf_failure(request, reason=""):
    # Redirigir al login si falla el CSRF (token invalido o faltante)
    messages.error(request, "Su sesión ha expirado o el token de seguridad es inválido. Por favor ingrese nuevamente.")
    return redirect('login')

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)
