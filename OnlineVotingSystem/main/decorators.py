from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import *
import datetime
import sweetify

def verified_or_superuser(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        profile = request.user
        if profile.verified or profile.is_superuser:
             return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('verify'))

  return wrap

def receipt_exist(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        profile = request.user
        if Receipt.objects.filter(owner=profile):
             return function(request, *args, **kwargs)
        else:
            sweetify.error(request, "Aún no tienes un recibo de votación")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  return wrap


def not_superuser(function):
     @wraps(function)
     def wrap(request, *args, **kwargs):
          profile = request.user
          if not profile.is_superuser:
               return function(request, *args, **kwargs)
          else:
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     return wrap

def department_not_voted_or_superuser(function):
     @wraps(function)
     def wrap(request, *args, **kwargs):
          profile = request.user
          if not profile.voted_department or profile.is_superuser:
               return function(request, *args, **kwargs)
          else:
               sweetify.error(request, '¡Ya has votado!')
               return HttpResponseRedirect(reverse('receipt'))
     return wrap


def ap_voter_or_superuser(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        profile = request.user
        if profile.department == 'AP' or profile.is_superuser:
          return function(request, *args, **kwargs)
        else:
          return HttpResponseRedirect('/')

  return wrap

def ap_schedule_or_superuser(function):
     @wraps(function)
     def wrap(request, *args, **kwargs):
          try:
               schedule = votingschedule.objects.get(department='AP')
               start = schedule.start
               end = schedule.end
               today = datetime.datetime.now().date()
               if today >= start and today <= end or request.user.is_superuser:
                    return function(request, *args, **kwargs)
               else:
                    sweetify.error(request, '¡Por favor espere el horario!')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
          except:
               sweetify.error(request, '¡Aún no hay ningún horario publicado!')
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     return wrap
