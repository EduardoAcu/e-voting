from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.hashers import make_password

class AccountManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = Account(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("last_name", " ")
        extra_fields.setdefault("first_name", "Administrador")

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class Account(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    department = models.TextField(choices=(('AP', 'AP'),), null=True)
    otp = models.IntegerField(null=True)
    verified = models.BooleanField(default=False)
    voted_department = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wallet_address = models.CharField(max_length=42, unique=True, null=True, blank=True)  # Dirección de la billetera
    private_key = models.TextField(null=True, blank=True)  # Clave privada (guardar de forma segura)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = AccountManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name
