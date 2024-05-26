# Generated by Django 5.0.3 on 2024-05-19 00:54

import django.db.models.deletion
import gestao_caixa.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registros_entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Registros_saida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMatricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_matricula', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TipoRecebimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_recebimento', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroSaida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('detalhe', models.TextField(blank=True, max_length=300)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_caixa.registros_saida')),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField(max_length=300)),
                ('sobrenome', models.TextField(max_length=300)),
                ('data_nascimento', models.DateTimeField()),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('cpf', models.CharField(max_length=14, unique=True, validators=[gestao_caixa.models.validate_cpf])),
                ('tipo_matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_caixa.tipomatricula')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroEntrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('detalhe', models.TextField(blank=True, max_length=300)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_caixa.aluno')),
                ('registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_caixa.registros_entrada')),
                ('tipo_recebimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao_caixa.tiporecebimento')),
            ],
        ),
    ]