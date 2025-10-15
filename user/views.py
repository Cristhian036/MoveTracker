from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


##################################################################
####################index#######################################
def index(request):
    return render(request, 'user/index.html',{'title':'index'})

########################################################################
########### register here #####################################

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            #########################mail####################################
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
            ##################################################################
            # Guardar el usuario
            user = form.save()
            
            # Asignar el rol de "usuario" al nuevo usuario
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

###################################################################################
################login forms###################################################

def Login(request):
    if request.method == 'POST':

        #AuthenticationForm_can_also_be_used__

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request,user)
            messages.success(request, f' wecome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'Credenciales inválidas')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form,'title':'log in'})
