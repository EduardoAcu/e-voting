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
    
    path('iei', views.ieiballot, name='iei'),
    path('iei/candidates', views.ieicandidates, name='ieicandidates'),
    path('iei/tally', views.ieitally, name='ieitally'),
    path('iei/result', views.ieiresult, name='ieiresult'),
    path('iei/candidate/update/<str:pk>', views.updateieicandidate, name='updateieicandidate'),
    path('iei/candidate/delete/<str:pk>', views.deleteieicandidate, name='deleteieicandidate'),
    
    path('ap/ballot', views.apballot, name='apballot'),
    path('ap/candidates', views.apcandidates, name='apcandidates'),
    path('ap/tally', views.aptally, name='aptally'),
    path('ap/result', views.apresult, name='apresult'),
    path('ap/candidate/update/<str:pk>', views.updateapcandidate, name='updateapcandidate'),
    path('ap/candidate/delete/<str:pk>', views.deleteapcandidate, name='deleteapcandidate'),
 
]
