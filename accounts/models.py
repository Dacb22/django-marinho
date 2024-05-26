from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import PermissionDenied
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, name, lastname, email, login, password=None, **extra_fields):
        if not extra_fields.get('is_superuser') and extra_fields.get('cargo') != Cargo.SOCIO:
            raise PermissionDenied('Somente sócios podem criar novos usuários.')

        user = self.model(
            name=name,
            lastname=lastname,
            email=email,
            login=login,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, lastname, email, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')

        return self.create_user(name, lastname, email, login, password, **extra_fields)


class Cargo(models.Model):
    RECEPCIONISTA = 'Recepcionista'
    PROFESSOR = 'Professor(a)'
    PROFESSOR_DANCA = 'Professor(a) de dança'
    PROFESSOR_CROSS = 'Professor(a) de crossfit'
    SOCIO = 'Sócio(a)'
    SERV_GERAIS = 'Serviços Gerais'

    OPCOES_CARGO = [
        (RECEPCIONISTA, 'Recepcionista'),
        (PROFESSOR, 'Professor(a)'),
        (PROFESSOR_DANCA, 'Professor(a) de dança'),
        (PROFESSOR_CROSS, 'Professor(a) de crossfit'),
        (SOCIO, 'Sócio(a)'),
        (SERV_GERAIS, 'Serviços Gerais'),
    ]

    nome = models.CharField(max_length=100, choices=OPCOES_CARGO)

    def __str__(self):
        return self.nome


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    login = models.CharField(max_length=255, unique=True)
    is_manager = models.BooleanField(default=False)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'lastname', 'email', 'cargo']

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.name} {self.lastname}"

    def get_short_name(self):
        return self.name
