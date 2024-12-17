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
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from web3 import Web3
from cryptography.fernet import Fernet

def landingpage(request):
    departments = ['AP']
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

# Asegúrate de que esta clave secreta esté almacenada de manera segura.
fernet_key = settings.FERNET_KEY  
cipher_suite = Fernet(fernet_key)

# Configuración de Web3 para conectar a Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Conexión a Ganache
assert web3.is_connected()

#Dirección de la cuenta origen en Ganache (cuenta con ETH de prueba)
from_account = "0x7590DBa733Fe29EBbC88A4B889Ae90F5bC54805a"  # Esta es la cuenta con ETH de prueba
private_key_from_account = "0x4e73f65e87a2a0d9b6447a00a885ec75fb6c7d02fd9fcd682a4b0a88788fb731"

# Función para transferir ETH de prueba desde una cuenta origen en Ganache a la nueva billetera
def transfer_eth_to_new_account(to_address):
    # Verificar saldo de la cuenta origen antes de hacer la transacción
    balance = web3.eth.get_balance(from_account)
    print(f"Saldo de la cuenta origen {from_account}: {web3.from_wei(balance, 'ether')} ETH")

    # Asegúrate de que haya suficiente saldo
    if balance < web3.to_wei(1, 'ether'):
        raise Exception("No hay suficiente saldo de ETH de prueba en la cuenta origen.")

    # Crear transacción para transferir 1 ETH de prueba
    transaction = {
        'to': to_address,
        'value': web3.to_wei(100, 'ether'),  # Enviar 1 ETH de prueba
        'gas': 21000,
        'gasPrice': web3.to_wei('1', 'gwei'),
        'nonce': web3.eth.get_transaction_count(from_account),
        'chainId': 1337  # Ganache usa la ID de cadena 1337
    }

    # Firmar la transacción
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key=private_key_from_account)

    # Enviar la transacción
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Esperar el recibo de la transacción
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Transacción completada con hash: {tx_receipt['transactionHash'].hex()}")


@receiver(post_save, sender=Account)
def create_wallet(sender, instance, created, **kwargs):
    if created:  # Solo se ejecuta cuando el usuario se crea
        # Crear una billetera de Ethereum para el usuario
        new_account = web3.eth.account.create()

        # Asignar la dirección pública de la billetera al usuario
        instance.wallet_address = new_account.address

        # Cifrar la clave privada antes de almacenarla en la base de datos
        encrypted_private_key = cipher_suite.encrypt(new_account.key).decode('utf-8')  # Cifrado de la clave privada

        # Asignar la clave privada cifrada al usuario
        instance.private_key = encrypted_private_key

        # Transferir 1 ETH de prueba de la cuenta de Ganache a la nueva billetera
        transfer_eth_to_new_account(new_account.address)

        # Guardar los cambios en el modelo de usuario
        instance.save()