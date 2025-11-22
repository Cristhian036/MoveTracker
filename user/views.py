from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import User
from .forms import UserRegisterForm, WorkerCreateForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


# Vista principal
def index(request):
    # Redirigir a dashboard si autenticado
    if request.user.is_authenticated:
        return redirect('parking:dashboard')
    return render(request, 'user/index.html',{'title':'index'})


# Registro de usuario
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            # Envio de correo
            htmly = get_template('user/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'hello', 'from@example.com', 'to@emaple.com'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("error en el envío del correo")
            
            # Guardar usuario
            user = form.save()
            
            # Asignar rol usuario
            try:
                usuario_group = Group.objects.get(name='usuario')
                user.groups.add(usuario_group)
                messages.success(request, f'¡Tu cuenta ha sido creada! Ya puedes iniciar sesión.')
            except Group.DoesNotExist:
                messages.warning(request, f'Your account has been created but the user role could not be assigned. Please contact an administrator.')
            
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form,'title':'reqister here'})


# Inicio de sesion
def Login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f' Bienvenido {username}!')
            return redirect('parking:dashboard')
        else:
            messages.info(request, f'Credenciales inválidas')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form,'title':'log in'})


# Gestion de trabajadores
def is_admin(user):
    # Verificar si es administrador
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name='administrador').exists()


@login_required
@user_passes_test(is_admin, login_url='login')
def worker_list(request):
    # Lista de trabajadores
    # Obtener grupo de trabajadores
    try:
        worker_group = Group.objects.get(name='trabajador')
        workers = User.objects.filter(groups=worker_group).order_by('username')
    except Group.DoesNotExist:
        workers = []
        messages.warning(request, 'El grupo "trabajador" no existe. Ejecuta python manage.py setup_roles')
    
    context = {
        'workers': workers,
        'title': 'Lista de Trabajadores',
        'total_workers': workers.count() if workers else 0
    }
    return render(request, 'user/worker_list.html', context)


@login_required
@user_passes_test(is_admin, login_url='login')
def worker_create(request):
    """Crear nuevo trabajador (solo admin)"""
    if request.method == 'POST':
        form = WorkerCreateForm(request.POST)
        if form.is_valid():
            worker = form.save()
            messages.success(request, f'Trabajador {worker.username} creado exitosamente.')
            return redirect('worker_list')
    else:
        form = WorkerCreateForm()
    
    context = {
        'form': form,
        'title': 'Crear Nuevo Trabajador'
    }
    return render(request, 'user/worker_form.html', context)


@login_required
@user_passes_test(is_admin, login_url='login')
def worker_delete(request, pk):
    """Eliminar trabajador (solo admin)"""
    worker = User.objects.get(pk=pk)
    
    # Verificar que sea un trabajador
    if not worker.groups.filter(name='trabajador').exists():
        messages.error(request, 'Este usuario no es un trabajador.')
        return redirect('worker_list')
    
    if request.method == 'POST':
        username = worker.username
        worker.delete()
        messages.success(request, f'Trabajador {username} eliminado exitosamente.')
        return redirect('worker_list')
    
    context = {
        'worker': worker,
        'title': 'Eliminar Trabajador'
    }
    return render(request, 'user/worker_confirm_delete.html', context)
