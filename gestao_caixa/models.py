import re

from accounts.models import Cargo
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Registros_entrada(models.Model):
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.descricao


class Registros_saida(models.Model):
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.descricao


class RegistroSaida(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    registro = models.ForeignKey(Registros_saida, on_delete=models.CASCADE)
    detalhe = models.TextField(max_length=300, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)


class TipoMatricula(models.Model):
    tipo_matricula = models.TextField(max_length=200)


class TipoRecebimento(models.Model):
    tipo_recebimento = models.TextField(max_length=200)


def validate_cpf(value):
    """
    Validates CPF using the standard algorithm.
    """
    cpf = re.sub(r'[^0-9]', '', value)  # Remove non-numeric characters

    if len(cpf) != 11 or not cpf.isdigit():
        raise ValidationError('CPF precisa ter 11 dígitos.')

    def calculate_digit(cpf, factor):
        total = sum(int(digit) * factor for digit, factor in zip(cpf, range(factor, 1, -1)))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)

    if cpf in ["00000000000", "11111111111", "22222222222", "33333333333",
               "44444444444", "55555555555", "66666666666", "77777777777",
               "88888888888", "99999999999"]:
        raise ValidationError('Invalid CPF.')

    first_digit = calculate_digit(cpf[:9], 10)
    second_digit = calculate_digit(cpf[:9] + first_digit, 11)

    if cpf[-2:] != first_digit + second_digit:
        raise ValidationError('CPF Inválido.')


class Aluno(models.Model):
    CHOICES_SEXO = {
        ('F', 'Feminino'),
        ('M', 'Masculino')
    }

    nome = models.TextField(max_length=300)
    sobrenome = models.TextField(max_length=300)
    tipo_matricula = models.ForeignKey(TipoMatricula, on_delete=models.CASCADE)
    data_nascimento = models.DateTimeField(null=False)
    sexo = models.CharField(max_length=1, choices=CHOICES_SEXO)
    cpf = models.CharField(
        max_length=14, unique=True, validators=[validate_cpf]
        )

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"


class RegistroEntrada(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    aluno = models.ForeignKey(Aluno, models.CASCADE)
    tipo_recebimento = models.ForeignKey(TipoRecebimento, models.CASCADE)
    registro = models.ForeignKey(Registros_entrada, on_delete=models.CASCADE)
    detalhe = models.TextField(max_length=300, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)


class Funcionario(models.Model):
    CHOICES_SEXO = {
        ('F', 'Feminino'),
        ('M', 'Masculino')
    }
    nome = models.TextField(max_length=300)
    sobrenome = models.TextField(max_length=300)
    cpf = models.CharField(
        max_length=14, unique=True, validators=[validate_cpf]
        )
    data_nascimento = models.DateTimeField(null=False)
    sexo = models.CharField(max_length=1, choices=CHOICES_SEXO)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True)


class Folha_Pagamento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateTimeField(null=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
