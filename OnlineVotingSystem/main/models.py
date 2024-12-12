from django.db import models
from account.models import *
import datetime
import string, secrets


def modalID_generator():
    alphabet = string.ascii_letters
    modalID = ''.join(secrets.choice(alphabet) for i in range(10))
    return modalID


class votingschedule(models.Model):
    department = models.TextField(choices=(
        ('IEI','IEI'),
        ('AP','AP')
        ), null=True)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.department}"

class IEI_Candidate(models.Model):
    modal_id = models.CharField(max_length=50, editable=False, default=modalID_generator)
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(null=True)
    position = models.TextField(choices=(
        ('Delegado Estudiantil','Delegado Estudiantil'),

        ), null=True)
    voters = models.ManyToManyField(Account, blank=True)

        
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/sb_admin/img/user.png"
    
    def __str__(self):
        return f"{self.fullname}"

class AP_Candidate(models.Model):
    modal_id = models.CharField(max_length=50, editable=False, default=modalID_generator)
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(null=True)
    position = models.TextField(choices=(
        ('Delegado Estudiantil','Delegado Estudiantil'),

        ), null=True)
    voters = models.ManyToManyField(Account, blank=True)

        
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/sb_admin/img/user.png"
    
    def __str__(self):
        return f"{self.fullname}"

class Receipt(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    delegado_estudiantil = models.CharField(max_length=50, blank=True, null=True)

    def get_owner(self):
        return self.owner.email

    def __str__(self):
        return f"{self.owner}"