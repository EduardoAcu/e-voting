from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('receipt', views.receipt, name='receipt'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),

    path('voters', views.voters, name='voters'),
    path('voters/update/<str:pk>', views.updatevoter, name='updatevoter'),
    path('voters/delete/<str:pk>', views.deletevoter, name='deletevoter'),

    path('election/schedule', views.electionschedule, name='electionschedule'),
    path('election/schedule/update/<str:pk>', views.updateelectionschedule, name='updateelectionschedule'),
    path('election/schedule/delete/<str:pk>', views.deleteelectionschedule, name='deleteelectionschedule'),
    
    path('mainssg', views.mainssgballot, name='mainssg'),
    path('mainssg/candidates', views.mainssgcandidates, name='mainssgcandidates'),
    path('mainssg/tally', views.mainssgtally, name='mainssgtally'),
    path('mainssg/result', views.mainssgresult, name='mainssgresult'),
    path('mainssg/candidate/update/<str:pk>', views.updatemainssgcandidate, name='updatemainssgcandidate'),
    path('mainssg/candidate/delete/<str:pk>', views.deletemainssgcandidate, name='deletemainssgcandidate'),
    
    path('ap/ballot', views.apballot, name='apballot'),
    path('ap/candidates', views.apcandidates, name='apcandidates'),
    path('ap/tally', views.aptally, name='aptally'),
    path('ap/result', views.apresult, name='apresult'),
    path('ap/candidate/update/<str:pk>', views.updateapcandidate, name='updateapcandidate'),
    path('ap/candidate/delete/<str:pk>', views.deleteapcandidate, name='deleteapcandidate'),
 
]
