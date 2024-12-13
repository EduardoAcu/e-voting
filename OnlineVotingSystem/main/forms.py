from django import forms
from pkg_resources import require
from .models import *

class IEI_CandidatesForm(forms.ModelForm):
   class Meta:
      model = IEI_Candidate
      exclude = ('voters',)
      fields = ('fullname', 'photo', 'bio', 'position')
      position_choices = (
        ('delegado','Delegado Estudiantil'),
      )
      widgets = {
         'photo': forms.FileInput(attrs={'type': 'file'}),
         'fullname':forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder':'Nombre Completo' }),
         'bio':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Cuéntanos sobre ti y tu lema.' }),
         'position':forms.Select(choices=position_choices,attrs={'class': 'form-control', 'placeholder':'Cargo' }),
      }

class AP_CandidatesForm(forms.ModelForm):
   class Meta:
      model = AP_Candidate
      exclude = ('voters',)
      fields = ('fullname', 'photo', 'bio', 'position')
      position_choices = (
        ('delegado','Delegado Estudiantil'),
      )
      widgets = {
         'photo': forms.FileInput(attrs={'type': 'file'}),
         'fullname':forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder':'Nombre Completo' }),
         'bio':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Cuéntanos sobre ti y tu lema.' }),
         'position':forms.Select(choices=position_choices,attrs={'class': 'form-control', 'placeholder':'Cargo' }),
      }

class ScheduleForm(forms.ModelForm):
   class Meta:
      model = votingschedule
      fields = ('department', 'start', 'end')
      widgets = {
         'department':forms.Select(attrs={'class': 'form-control' }),
         'start':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
         'end':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
      }

class UpdateScheduleForm(forms.ModelForm):
   class Meta:
      model = votingschedule
      exclude = ('department',)
      fields = ('start', 'end')
      widgets = {
         'start':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
         'end':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
      }


