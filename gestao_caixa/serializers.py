from accounts.models import User
from django.utils import timezone
from rest_framework import serializers

from .models import (Aluno, Cargo, Folha_Pagamento, Funcionario,
                     RegistroEntrada, Registros_entrada, Registros_saida,
                     RegistroSaida, TipoMatricula, TipoRecebimento)


class RegistrosEntradaSerializer(serializers.ModelSerializer):
    descricao = serializers.ReadOnlyField(source='registro.descricao')
    data = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', default_timezone=timezone.get_current_timezone())

    class Meta:
        model = RegistroEntrada
        fields = ['id', 'valor', 'descricao', 'tipo_recebimento_id', 'aluno', 'detalhe', 'data', 'user_id']
        read_only_fields = ['id', 'data']


class RegistrosSaidaSerializer(serializers.ModelSerializer):
    descricao = serializers.ReadOnlyField(source='registro.descricao')
    data = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', default_timezone=timezone.get_current_timezone())

    class Meta:
        model = RegistroSaida
        fields = ['id', 'valor', 'descricao', 'detalhe', 'data', 'user_id']
        read_only_fields = ['id', 'data']


class RegistrosListaSaidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroSaida
        fields = ['registro', 'valor', 'data']
        read_only_fields = ['id', 'data']


class RegistrosListaEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroEntrada
        fields = ['registro', 'aluno', 'valor', 'data']
        read_only_fields = ['id', 'data']


class RegistrosListaSaidasCadastradasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registros_saida
        fields = ['id', 'descricao']


class RegistrosListaEntradasCadastradasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registros_saida
        fields = ['id', 'descricao']


class RegistrosListaMatriculasCadastradasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMatricula
        fields = ['id', 'tipo_matricula']


class RegistrosAlunosCadastradosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'sobrenome', 'data_nascimento', 'sexo', 'tipo_matricula_id']


class RegistroAlunoSerializer(serializers.ModelSerializer):
    tipo_matricula_id = serializers.ReadOnlyField(source='tipo_matricula_id.tipo_matricula')
    data_nascimento = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', default_timezone=timezone.get_current_timezone())

    class Meta:
        model = Aluno
        fields = ['nome', 'sobrenome', 'data_nascimento', 'sexo', 'tipo_matricula_id', 'cpf']
        read_only_fields = ['id']

class RecebimentosCadastradosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRecebimento
        fields = ['id', 'tipo_recebimento']


class CargosCadastradosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id', 'nome']


class FuncionariosCadastradosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'sobrenome', 'cpf', 'data_nascimento', 'sexo', 'cargo_id']


class FolhaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folha_Pagamento
        fields = ('id', 'data', 'valor', 'funcionario_id')


class UsuariosCadastradosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
