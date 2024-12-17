from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from account.models import *
from .forms import *
from django.db.models import F
import sweetify
from account.forms import *
from main.decorators import *
import datetime
from django.conf import settings
from solcx import compile_source
import hashlib
import qrcode
from main.connect_blockchain import *
from .desencription import decrypt_private_key
from google.cloud import storage



def landingpage(request):
    return render(request, 'landingpage/landingpage.html')  


@login_required(login_url='login')
def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'main/home.html', context)

@login_required(login_url='login')
@verified_or_superuser
@receipt_exist
def receipt(request):
    context = {
        'title': 'Receipt',
        'receipts': Receipt.objects.filter(owner=request.user)

    }
    return render(request, 'main/receipt.html', context)

@user_passes_test(lambda u: u.is_superuser)
def voters(request):
    context = {
        'title': 'Voters',
        'voters': Account.objects.filter(is_superuser=False)
    }
    return render(request, 'main/voters.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updatevoter(request, pk):
    voter = Account.objects.get(id=pk)
    voterform = RegistrationForm(instance=voter)
    if request.method == 'POST':
        voterform = RegistrationForm(request.POST, instance=voter)
        if voterform.is_valid():
            voterform.save()
            return HttpResponseRedirect(reverse('voters'))

    context = {
        'title': 'Update Voter',
        'voter': voter,
        'form': voterform,
    }
    
    return render(request, 'main/voterupdate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletevoter(request, pk):
    voter = Account.objects.get(id=pk)
    context = {
        'title': 'Delete Voter',
        'voter': voter,
    }
    if request.method == 'POST':
        voter.delete()
        return HttpResponseRedirect(reverse('voters'))
    return render(request, 'main/voterdelete.html', context)



@login_required(login_url='login')
@verified_or_superuser
def profile(request, pk):
    profile = Account.objects.get(id=pk)
    student_form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        student_form = UpdateProfileForm(request.POST, instance=profile)
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 != password2:
            print("password does not match")
            sweetify.error(request, 'Password does not match!')
            return HttpResponseRedirect(request.path_info)
        elif student_form.is_valid():
            student_form.save()
            sweetify.success(request, 'Updated Successfully')
            return HttpResponseRedirect(reverse('login'))
        else: 
            sweetify.error(request, 'Invalid Credentials!')
            return HttpResponseRedirect(request.path_info)
    context = {
        'title': 'Profile',
        'student_form': student_form,
        'profile': profile,
    }
    return render(request, 'main/profile.html', context)


@user_passes_test(lambda u: u.is_superuser)
def electionschedule(request):
    schedule_form = ScheduleForm()
    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
            return HttpResponseRedirect(reverse('electionschedule'))
    context = {
        'title': 'Schedule',
        'schedule': votingschedule.objects.all(),
        'schedule_form': schedule_form,
    }
    return render(request, 'main/electionschedule.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updateelectionschedule(request, pk):
    schedule = votingschedule.objects.get(id=pk)
    schedule_form = UpdateScheduleForm(instance=schedule)
    context = {
        'title': 'Update Schedule',
        'schedule': schedule,
        'schedule_form': schedule_form
    }
    if request.method == 'POST':
        schedule_form = UpdateScheduleForm(request.POST, instance=schedule)
        if schedule_form.is_valid():
            schedule_form.save()
            return HttpResponseRedirect(reverse('electionschedule'))
    return render(request, 'main/updateelectionschedule.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deleteelectionschedule(request, pk):
    schedule = votingschedule.objects.get(id=pk)
    context = {
        'title': 'Delete Shedule',
        'schedule': schedule,
    }
    if request.method == 'POST':
        schedule.delete()
        return HttpResponseRedirect(reverse('electionschedule'))
    return render(request, 'main/deleteschedule.html', context)


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    apcandidates = AP_Candidate.objects.all().count()
    totalcandidates =  apcandidates
    voted_department = Account.objects.filter(voted_department=True).count()
    context = {
        'title': 'Dashboard',

        'totalcandidates': totalcandidates,

        'ap': AP_Candidate.objects.all(),
        'apcandidates': apcandidates,
    
        'registered': Account.objects.filter(is_superuser=False).count(),
        'voted': voted_department
    }
    return render(request, 'main/dashboard.html', context)



############################################################################################################

@user_passes_test(lambda u: u.is_superuser)
def apcandidates(request):
    candidate_form = AP_CandidatesForm()
    if request.method == 'POST':
        candidate_form = AP_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("apcandidates"))

    context = {
        'title': 'Candidatos de Analista Progamador',
        'form': candidate_form,
        'ap': AP_Candidate.objects.all()
    }
    return render(request, 'main/apcandidates.html', context) 

@user_passes_test(lambda u: u.is_superuser)
def updateapcandidate(request, pk):
    candidate = AP_Candidate.objects.get(id=pk)
    candidate_form = AP_CandidatesForm(instance=candidate)
    context = {
                'title': 'Actualizar Candidatos de Analista Programador',
                'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = AP_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('apcandidates'))
    return render(request, 'main/apupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deleteapcandidate(request, pk):
    apcandidate = AP_Candidate.objects.get(id=pk)
    context = {
        'title': 'Eliminar Candidatos de Analista Programador',
        'apcandidate': apcandidate,
    }
    if request.method == 'POST':
        apcandidate.delete()
        return HttpResponseRedirect(reverse('apcandidates'))

    return render(request, 'main/apdeletecandidate.html', context)



@user_passes_test(lambda u: u.is_superuser)
def aptally(request):
    context = {
        'title': 'Resumen Total',
        'ap': AP_Candidate.objects.all(),
    }
    return render(request, 'main/aptally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def apresult(request):
    context = {
        'title': 'Resultado de Analista Programador',
        'delegado': AP_Candidate.objects.filter(position='delegado'),
    }
    return render(request, 'main/apresult.html', context)


@login_required(login_url='login')
@verified_or_superuser
@ap_voter_or_superuser
@department_not_voted_or_superuser
def apballot(request):
    context = {
        'title': 'receipts',
        'delegado': AP_Candidate.objects.filter(position='delegado'),
    }

    if request.method == 'POST':
        voter = request.user

        # Obtener la dirección de la billetera del votante
        wallet_address = voter.wallet_address  # Dirección pública de la billetera

        # Obtener la clave privada cifrada
        encrypted_private_key = voter.private_key  # La clave privada cifrada de la base de datos

        # Desencriptar la clave privada
        private_key = decrypt_private_key(encrypted_private_key)

        # Verificar si el votante ya ha votado
        has_voted = contract.functions.hasVoted(wallet_address).call()
        if has_voted:
            sweetify.error(request, '¡Ya has votado anteriormente!')
            return render(request, 'main/apballot.html', context)

        # Validar si el usuario seleccionó un delegado
        try:
            voted_delegado = request.POST["delegado"]
            g_voted = AP_Candidate.objects.get(fullname=voted_delegado)
            g_voters = g_voted.voters
            g_voters.add(voter)

            # Crear el hash del voto
            vote_hash = hashlib.sha256(f"{voter.email}-{voted_delegado}".encode()).hexdigest()

            balance = web3.eth.get_balance(wallet_address)
            print(f"Saldo de la cuenta {wallet_address}: {web3.from_wei(balance, 'ether')} ETH")

            # Asegúrate de que haya suficiente saldo para cubrir el gas
            required_gas = web3.to_wei(0.01, 'ether')  # Estimación del gas que la transacción va a consumir
            if balance < required_gas:
                raise Exception("Saldo insuficiente para cubrir el gas de la transacción.")

            # Construir la transacción para interactuar con el contrato
            tx = contract.functions.castVote(voted_delegado, vote_hash).build_transaction({
                'from': wallet_address,
                'gas': 150000,
                'gasPrice': web3.to_wei('1', 'gwei'),
                'nonce': web3.eth.get_transaction_count(wallet_address),
            })

            # Firmar la transacción con la clave privada desencriptada
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Esperar el recibo de la transacción
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            # Generar el QR para la transacción
            tx_url = f"https://etherscan.io/tx/{tx_hash.hex()}"
            qr = qrcode.make(tx_url)

            # Conectar con Google Cloud Storage
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(settings.GS_BUCKET_NAME)
            
            # Usar un nombre único para el archivo (por ejemplo, basado en el hash del voto)
            qr_blob = bucket.blob(f"qrcodes/{vote_hash}.png")
            
            # Subir el archivo QR al bucket de Google Cloud
            qr_path = '/tmp/qr.png'  # Ruta temporal para guardar el QR antes de subirlo
            qr.save(qr_path)
            qr_blob.upload_from_filename(qr_path)

            # URL pública del QR almacenado en Google Cloud Storage
            qr_url = qr_blob.public_url

            # Guardar en el modelo Receipt
            receipt, created = Receipt.objects.get_or_create(owner=voter, department=voter.department)
            receipt.delegado = voted_delegado
            receipt.delegado_hash = vote_hash
            receipt.blockchain_tx = tx_hash.hex()
            receipt.qr_path = qr_url  # Usar la URL pública del QR
            receipt.save()

            # Marcar al votante como que ya votó
            voter.voted_department = True
            voter.save()

            sweetify.success(request, '¡Votación enviada con éxito!')

            # Redirigir después de votar
            return HttpResponseRedirect(reverse('home'))

        except KeyError:
            sweetify.error(request, 'Ningún Delegado Estudiantil seleccionado')

    return render(request, 'main/apballot.html', context)
    
###############################################################################################################################################################


@user_passes_test(lambda u: u.is_superuser)
def settings(request):
    if request.method == 'POST': 
        ### AP ####

        try:
            reset_ap = request.POST['reset_ap']
            candidates = AP_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, '¡Se restablecio correctamente las elecciones de Analista Programador!')
        except:
            print('No se puede restablecer la carrera de Analista Programador')
        try:
            delete_ap = request.POST['delete_ap']
            candidates = AP_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, '¡Los delegados estudiantiles de Analista Programador fueron eliminados!') 
        except:
            print('No se pueden restablecer los delegados de Analista Programador')

    context = {
        'title': 'Settings'
    }
    return render(request, 'main/settings.html', context)

