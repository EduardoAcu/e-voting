from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from main.models import *
from django.conf import settings
import sweetify
import random as r
import smtplib
from datetime import date



def landingpage(request):
    departments = ['IEI','AP']
    schedules = votingschedule.objects.all()
    
    # Generar el contexto dinámicamente
    department_schedules = {
        department.lower(): votingschedule.objects.filter(department=department).first() or 'Sin horario'
        for department in departments
    }

    context = {
        **department_schedules,  # Desempaquetar los horarios de departamentos
        'today': date.today(),
        'schedules': schedules if schedules.exists() else []
    }

    return render(request, 'account/landingpage.html', context)


def generate_otp():
    # Generar un OTP con longitud entre 5 y 8, incluyendo el 0 como dígito válido
    length = r.randint(5, 8)
    otp = ''.join(str(r.randint(0, 9)) for _ in range(length))
    return otp

print(generate_otp())  # Ejemplo de salida: '83425' o '1928376'


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if settings.OTP:
                login(request, user)
                if user.verified:
                    sweetify.success(request, 'Inicio sesión exitosamente')
                    return HttpResponseRedirect(reverse('home'))
                elif user.is_superuser:
                    sweetify.success(request, 'Inicio sesión exitosamente')
                    return HttpResponseRedirect(reverse('dashboard'))
                elif not user.verified:
                    login(request, user)
                    user = request.user
                    otp = generate_otp()
                    user.otp = otp
                    user.save()
                    try:
                        SENDER_EMAIL = settings.OTP_EMAIL
                        SENDER_PASSWORD = settings.OTP_PASSWORD
                        SUBJECT = "OTP Verification"
                        TEXT = otp
                        MESSAGE = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                        RECEIVER_EMAIL = email
                        SERVER = smtplib.SMTP('smtp.gmail.com', 587)
                        SERVER.starttls()
                        SERVER.login(SENDER_EMAIL, SENDER_PASSWORD)
                        SERVER.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, MESSAGE)
                    except:
                        return HttpResponseRedirect(reverse('verify'))
                    sweetify.success(request, 'Revisa tu correo electrónico para verificación')
                    return HttpResponseRedirect(reverse('verify'))
            else:
                #Bypass OTP
                login(request, user)
                user = request.user
                user.verified = True
                Receipt.objects.create(owner=user, department="Carrera")
                Receipt.objects.create(owner=user, department=user.department)
                user.save()
                sweetify.success(request, 'Inicio sesión exitosamente')
                return HttpResponseRedirect(reverse('home'))
        else:
            sweetify.error(request, 'Credenciales inválidas')
            return render(request, 'account/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'account/login.html')


def verify(request):
    otp_form = VerificationForm()
    context = {
        'otp_form': otp_form
    }
    if request.method == 'POST':
        user = request.user
        otp_form = VerificationForm(request.POST)
        user_otp = request.POST['otp']
        otp = int(user_otp)
        if otp == user.otp:
            user = request.user
            user.verified = True
            Receipt.objects.create(owner=user, department=user.department)
            Receipt.objects.create(owner=user, department='Carrera')
            user.save()
            sweetify.success(request, 'Inicio sesión exitosamente')
            return HttpResponseRedirect(reverse('home'))
        else:
            print("failed")
            return render(request, 'account/verify.html', {'error': 'La OTP es incorrecta!', 'otp_form': otp_form})

    return render(request, 'account/verify.html', context)


def register_view(request):
    Registration_Form = RegistrationForm()
    if request.method == 'POST':
        Registration_Form = RegistrationForm(request.POST)
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 != password2:
            sweetify.error(request, '¡La contraseña no coincide!')
            return render(request, 'account/register.html', {'error': '¡La contraseña no coincide!', 'Registration_Form':Registration_Form})
        elif Registration_Form.is_valid():
            Registration_Form.save()
            sweetify.success(request, 'Registro exitoso')
            return HttpResponseRedirect(reverse('login'))
        elif Account.objects.filter(email=email).exists():
            sweetify.error(request, '¡El correo electrónico ya existe!')
            return render(request, 'account/register.html', {'error': '¡El correo electrónico ya existe!','Registration_Form':Registration_Form})
        else:
            sweetify.error(request, 'Credenciales inválidas')
            return render(request, 'account/register.html', {'error': 'Credenciales inválidas','Registration_Form':Registration_Form})
    return render(request, 'account/register.html', {'Registration_Form':Registration_Form})


def logout_view(request):
    logout(request)
    return render(request, 'account/login.html')

