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
    ieicandidates =  IEI_Candidate.objects.all().count()
    apcandidates = AP_Candidate.objects.all().count()
    totalcandidates = ieicandidates + apcandidates
    voted_department = Account.objects.filter(voted_department=True).count()
    voted_main = Account.objects.filter(voted_main=True).count()
    context = {
        'title': 'Dashboard',

        'totalcandidates': totalcandidates,

        'iei': IEI_Candidate.objects.all(),
        'ieicandidates': ieicandidates,

        'ap': AP_Candidate.objects.all(),
        'apcandidates': apcandidates,
    
        'registered': Account.objects.filter(is_superuser=False).count(),
        'voted': voted_department + voted_main,
    }
    return render(request, 'main/dashboard.html', context)



############################################################################################################

@user_passes_test(lambda u: u.is_superuser)
def ceitcandidates(request):
    candidate_form = AP_CandidatesForm()
    if request.method == 'POST':
        candidate_form = AP_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("apcandidates"))

    context = {
        'title': 'CEIT Candidates',
        'form': candidate_form,
        'ceit': AP_Candidate.objects.all()
    }
    return render(request, 'main/ceitcandidates.html', context) 

@user_passes_test(lambda u: u.is_superuser)
def updateceitcandidate(request, pk):
    candidate = AP_Candidate.objects.get(id=pk)
    candidate_form = AP_CandidatesForm(instance=candidate)
    context = {
                'title': 'Update CEIT Candidate',
                'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = AP_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('ceitcandidates'))
    return render(request, 'main/ceitupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deleteceitcandidate(request, pk):
    ceitcandidate = AP_Candidate.objects.get(id=pk)
    context = {
        'title': 'Delete CEIT Candidate',
        'ceitcandidate': ceitcandidate,
    }
    if request.method == 'POST':
        ceitcandidate.delete()
        return HttpResponseRedirect(reverse('ceitcandidates'))

    return render(request, 'main/ceitdeletecandidate.html', context)



@user_passes_test(lambda u: u.is_superuser)
def ceittally(request):
    context = {
        'title': 'CEIT Tally',
        'ceit': AP_Candidate.objects.all(),
    }
    return render(request, 'main/ceittally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def ceitresult(request):
    context = {
        'title': 'CEIT Result',
        'governor': AP_Candidate.objects.filter(position='Governor'),
    }
    return render(request, 'main/ceitresult.html', context)



@login_required(login_url='login')
@verified_or_superuser
@ap_voter_or_superuser
@department_not_voted_or_superuser
@ap_schedule_or_superuser
def ceitballot(request):
    context = {
        'title': 'CEIT Ballot',
        'governor': AP_Candidate.objects.filter(position='Governor'),
    }
    if request.method == 'POST':
        voter = request.user
        voter.voted_department = True
        voter.save()
        sweetify.success(request, 'Vote Submitted!')


    ###### GOVERNOR ######
    try: 
        request.POST['governor']
        voted_governor = request.POST["governor"]
        g_voted = AP_Candidate.objects.get(fullname=voted_governor)
        g_voters = g_voted.voters
        g_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.governor = voted_governor
        receipt.save()

    except:
        print("No selected Governor")
    
    return render(request, 'main/ceitballot.html', context)
    
###############################################################################################################################################################

@user_passes_test(lambda u: u.is_superuser)
def mainssgcandidates(request):
    candidate_form = IEI_CandidatesForm()
    if request.method == 'POST':
        candidate_form = IEI_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("mainssgcandidates"))

    context = {
        'title': 'Main SSG Candidates',
        'form': candidate_form,
        'mainssg': IEI_Candidate.objects.all()
    }
    return render(request, 'main/mainssgcandidates.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updatemainssgcandidate(request, pk):
    candidate = IEI_Candidate.objects.get(id=pk)
    candidate_form = IEI_CandidatesForm(instance=candidate)
    context = {
                'title': 'Update Main SSG Candidate',
                'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = IEI_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('mainssgcandidates'))
    return render(request, 'main/mainssgupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletemainssgcandidate(request, pk):
    mainssgcandidate = IEI_Candidate.objects.get(id=pk)
    context = {
        'title': 'Delete Main SSG Candidate',
      'mainssgcandidate': mainssgcandidate,
    }
    if request.method == 'POST':
        mainssgcandidate.delete()
        return HttpResponseRedirect(reverse('mainssgcandidates'))

    return render(request, 'main/mainssgeletecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def mainssgtally(request):
    context = {
        'title': 'Main SSG Tally',
        'mainssg': IEI_Candidate.objects.all(),
    }
    return render(request, 'main/mainssgtally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def mainssgresult(request):
    context = {
        'title': 'Main SSG Result',
        'governor': IEI_Candidate.objects.filter(position='Governor'),
    }
    return render(request, 'main/mainssgresult.html', context)



@login_required(login_url='login')
@verified_or_superuser
@iei_schedule_or_superuser
@iei_not_voted_or_superuser
def mainssgballot(request):
    context = {
        'title': 'Main SSG Ballot',
        'governor': IEI_Candidate.objects.filter(position='Governor'),
    }
    if request.method == 'POST':
        voter = request.user
        voter.voted_main = True
        voter.save()
        sweetify.success(request, 'Vote Submitted!')
        
        

     ###### GOVERNOR ######
    try: 
        request.POST['governor']
        voted_governor = request.POST["governor"]
        g_voted = IEI_Candidate.objects.get(fullname=voted_governor)
        g_voters = g_voted.voters
        g_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.governor = voted_governor
        receipt.save()

    except:
        print("No selected Governor")

    return render(request, 'main/mainssgballot.html', context)


@user_passes_test(lambda u: u.is_superuser)
def settings(request):
    if request.method == 'POST':
        ### MAIN ####
        try:
            reset_main = request.POST['reset_main']
            candidates = IEI_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, 'Main SSG Election successfully reset!')
        except:
            print('Cannot Reset Main Branch')
        try:
            delete_main = request.POST['delete_main']
            candidates = IEI_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, 'Main SSG Candidates successfully deleted!')
        except:
            print('Cannot Reset Main Branch')

        
        ### CEIT ####

        try:
            reset_ceit = request.POST['reset_ceit']
            candidates = AP_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, 'CEIT Election successfully reset!')
        except:
            print('Cannot Reset CEIT Department')
        try:
            delete_ceit = request.POST['delete_ceit']
            candidates = AP_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, 'CEIT Candidates successfully deleted!')
        except:
            print('Cannot Reset CEIT Department')

    context = {
        'title': 'Settings'
    }
    return render(request, 'main/settings.html', context)