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
from web3 import Web3
from solcx import compile_source
import hashlib
import qrcode


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
    voted_iei = Account.objects.filter(voted_iei=True).count()
    context = {
        'title': 'Dashboard',

        'totalcandidates': totalcandidates,

        'ap': AP_Candidate.objects.all(),
        'apcandidates': apcandidates,
    
        'registered': Account.objects.filter(is_superuser=False).count(),
        'voted': voted_department + voted_iei,
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


# Configurar Web3 con Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # URL de Ganache
assert web3.is_connected()

# ABI y dirección del contrato desplegado (utiliza la dirección de tu contrato desplegado)
contract_address = "0xc36637eA49Cd0AaaaFd5b82F90AC541527E4f0cD"  # Reemplaza con la dirección de tu contrato
contract_abi = [{'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'voter', 'type': 'address'}, {'indexed': False, 'internalType': 'string', 'name': 'candidate', 'type': 'string'}, {'indexed': False, 'internalType': 'string', 'name': 'voteHash', 'type': 'string'}, {'indexed': False, 'internalType': 'uint256', 'name': 'timestamp', 'type': 'uint256'}], 'name': 'VoteCast', 'type': 'event'}, {'inputs': [{'internalType': 'string', 'name': '_candidate', 'type': 'string'}, {'internalType': 'string', 'name': '_voteHash', 'type': 'string'}], 'name': 'castVote', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': '_voteHash', 'type': 'string'}], 'name': 'getVote', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'string', 'name': '', 'type': 'string'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'hasVoted', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'name': 'votes', 'outputs': [{'internalType': 'address', 'name': 'voter', 'type': 'address'}, {'internalType': 'string', 'name': 'candidate', 'type': 'string'}, {'internalType': 'uint256', 'name': 'timestamp', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}]  # ABI del contrato

contract = web3.eth.contract(address=contract_address, abi=contract_abi)


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
        
        # Validar si el usuario seleccionó un delegado
        try:
            # Obtener el delegado seleccionado
            voted_delegado = request.POST["delegado"]
            g_voted = AP_Candidate.objects.get(fullname=voted_delegado)
            g_voters = g_voted.voters
            g_voters.add(voter)

            # Crear el hash del voto
            vote_hash = hashlib.sha256(f"{voter.email}-{voted_delegado}".encode()).hexdigest()

            # Construir la transacción para interactuar con el contrato
            tx = contract.functions.castVote(voted_delegado, vote_hash).buildTransaction({
                'from': web3.eth.default_account,
                'gas': 3000000,
                'gasPrice': web3.toWei('50', 'gwei'),
                'nonce': web3.eth.getTransactionCount(web3.eth.default_account),
            })

            # Firmar la transacción
            signed_tx = web3.eth.account.signTransaction(tx, private_key="0xfd94cdf551d58c04b5e8e83ac550904a9a421fe669e247b79fecd8f291bbdf2c")  # Reemplaza con la clave privada
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            # Esperar el recibo de la transacción
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            # Generar el QR para la transacción
            tx_url = f"https://etherscan.io/tx/{tx_hash.hex()}"
            qr = qrcode.make(tx_url)
            qr_path = f"media/qrcodes/{vote_hash}.png"
            qr.save(qr_path)

            # Guardar en el modelo Receipt
            receipt, created = Receipt.objects.get_or_create(owner=voter, department=voter.department)
            receipt.delegado = voted_delegado
            receipt.delegado_hash = vote_hash
            receipt.blockchain_tx = tx_hash.hex()
            receipt.qr_path = qr_path
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

