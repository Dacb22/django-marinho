from datetime import datetime

from accounts.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Aluno, Cargo, Folha_Pagamento, Funcionario,
                     RegistroEntrada, Registros_entrada, Registros_saida,
                     RegistroSaida, TipoMatricula, TipoRecebimento)
from .serializers import (CargosCadastradosSerializer,
                          FolhaPagamentoSerializer,
                          FuncionariosCadastradosSerializer,
                          RecebimentosCadastradosSerializer,
                          RegistroAlunoSerializer,
                          RegistrosAlunosCadastradosSerializer,
                          RegistrosEntradaSerializer,
                          RegistrosListaEntradasCadastradasSerializer,
                          RegistrosListaEntradaSerializer,
                          RegistrosListaMatriculasCadastradasSerializer,
                          RegistrosListaSaidasCadastradasSerializer,
                          RegistrosListaSaidaSerializer,
                          RegistrosSaidaSerializer,
                          UsuariosCadastradosSerializer)


class NovaEntrada(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        descricao = request.data.get('registro')
        valor = request.data.get('valor')
        aluno_id = request.data.get('aluno_id')
        tipo_recebimento = request.data.get('tipo_recebimento')
        user_id = request.data.get('user_id')
        # Encontrar a instância de Registros_saida com base na descrição
        try:
            registro_entrada = Registros_entrada.objects.get(descricao=descricao)
        except Registros_entrada.DoesNotExist:
            return Response(
                {"error": f"Registro de entrada com descrição '{descricao}' não encontrado(a)."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            tipo_recebimento = TipoRecebimento.objects.get(tipo_recebimento=tipo_recebimento)
        except TipoRecebimento.DoesNotExist:
            return Response(
                {"error": f"Tipo de recebimento com descrição '{tipo_recebimento}' não encontrado(a)."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Obter o objeto Aluno com base no aluno_id fornecido
        aluno = get_object_or_404(Aluno, id=aluno_id)

        # Criar a nova entrada de registro
        nova_entrada = RegistroEntrada.objects.create(registro=registro_entrada, tipo_recebimento=tipo_recebimento, aluno=aluno, valor=valor, user_id=user_id)
        nova_entrada.save()

        serializer = RegistrosEntradaSerializer(nova_entrada)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NovaSaida(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        descricao = request.data.get('registro')
        valor = request.data.get('valor')
        user_id = request.data.get('user_id')
        # Encontrar a instância de Registros_saida com base na descrição
        try:
            registro_saida = Registros_saida.objects.get(descricao=descricao)
        except Registros_saida.DoesNotExist:
            return Response(
                {"error": f"Registro de saída com descrição '{descricao}' não encontrado(a)."},
                status=status.HTTP_404_NOT_FOUND
            )

        nova_saida = RegistroSaida.objects.create(registro=registro_saida, valor=valor, user_id=user_id)
        nova_saida.save()

        serializer = RegistrosSaidaSerializer(nova_saida)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListaEntradas(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entradas = RegistroEntrada.objects.all()
        serializer = RegistrosEntradaSerializer(entradas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EditarEntrada(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, entrada_id):
        try:
            entrada = RegistroEntrada.objects.get(id=entrada_id)
        except RegistroEntrada.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RegistrosEntradaSerializer(entrada, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExcluirEntrada(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, entrada_id):
        try:
            entrada = RegistroEntrada.objects.get(id=entrada_id)
        except RegistroEntrada.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        entrada.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExcluirSaida(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, entrada_id):
        try:
            saida = RegistroSaida.objects.get(id=entrada_id)
        except RegistroSaida.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        saida.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListaSaidas(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saidas = RegistroSaida.objects.all()
        serializer = RegistrosSaidaSerializer(saidas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
 

class ListaSaidasCadastradas(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saidas = Registros_saida.objects.all()
        serializer = RegistrosListaSaidasCadastradasSerializer(saidas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ListaEntradasCadastradas(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saidas = Registros_entrada.objects.all()
        serializer = RegistrosListaEntradasCadastradasSerializer(saidas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ListaMatriculasCadastradas(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saidas = TipoMatricula.objects.all()
        serializer = RegistrosListaMatriculasCadastradasSerializer(saidas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NovoTipoMatricula(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        descricao = request.data.get('tipo_matricula')

        # Encontrar a instância de Registros_saida com base na descrição
        try:
            registro_tipo_matricula = TipoMatricula.objects.get(tipo_matricula=descricao)
        except TipoMatricula.DoesNotExist:
            return Response(
                {"error": f"Tipo de Matrícula com descrição '{descricao}' não encontrado(a)."},
                status=status.HTTP_404_NOT_FOUND
            )

        novo_tipo_matricula = RegistroSaida.objects.create(tipo_matricula=registro_tipo_matricula)
        novo_tipo_matricula.save()

        serializer = RegistrosSaidaSerializer(novo_tipo_matricula)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AlunosCadastrados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alunos = Aluno.objects.all()
        serializer = RegistrosAlunosCadastradosSerializer(alunos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RecebimentosCadastrados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recebimentos = TipoRecebimento.objects.all()
        serializer = RecebimentosCadastradosSerializer(recebimentos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NovoTipoRecebimento(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tipo_recebimento = request.data.get('tipo_recebimento')

        # Encontrar a instância de Registros_saida com base na descrição
        if TipoRecebimento.objects.filter(tipo_recebimento=tipo_recebimento).exists():
            return Response(
                {"error": "Tipo Recebimento já existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar um novo tipo Recebimento
        try:
            novo_tipo_recebimento = TipoRecebimento.objects.create(
                tipo_recebimento=tipo_recebimento
            )
            novo_tipo_recebimento.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RecebimentosCadastradosSerializer(novo_tipo_recebimento)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NovoTipoSaida(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        descricao = request.data.get('descricao')

        # Encontrar a instância de Registros_saida com base na descrição
        if Registros_saida.objects.filter(descricao=descricao).exists():
            return Response(
                {"error": "Tipo Saída já existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar um novo tipo Recebimento
        try:
            novo_tipo_saida = Registros_saida.objects.create(
                descricao=descricao
            )
            novo_tipo_saida.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RegistrosListaSaidasCadastradasSerializer(novo_tipo_saida)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NovoTipoEntrada(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        descricao = request.data.get('descricao')

        # Encontrar a instância de Registros_saida com base na descrição
        if Registros_entrada.objects.filter(descricao=descricao).exists():
            return Response(
                {"error": "Tipo Entrada já existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar um novo tipo Recebimento
        try:
            novo_tipo_entrada = Registros_entrada.objects.create(
                descricao=descricao
            )
            novo_tipo_entrada.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RegistrosListaEntradasCadastradasSerializer(novo_tipo_entrada)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NovoAluno(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nome = request.data.get('nome')
        sobrenome = request.data.get('sobrenome')
        data_nascimento = request.data.get('data_nascimento')
        sexo = request.data.get('sexo')
        tipo_matricula_id = request.data.get('tipo_matricula_id')
        cpf = request.data.get('cpf')

        # Validar se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return Response(
                {"error": "CPF precisa ter exatamente 11 dígitos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Converter data do formato brasileiro para o formato ISO
        try:
            data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y')
        except ValueError:
            return Response(
                {"error": "Data de nascimento inválida. Use o formato dd/mm/yyyy."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Converter a data de nascimento para um datetime com fuso horário UTC
        data_nascimento = timezone.make_aware(data_nascimento)

        # Encontrar a instância de Aluno com base no CPF
        if Aluno.objects.filter(cpf=cpf).exists():
            return Response(
                {"error": "CPF já está em uso."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar um novo aluno
        try:
            novo_aluno = Aluno.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                data_nascimento=data_nascimento,
                sexo=sexo,
                tipo_matricula_id=tipo_matricula_id,
                cpf=cpf
            )
            novo_aluno.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serializar e retornar os dados do novo aluno
        serializer = RegistroAlunoSerializer(novo_aluno)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListaCargosCadastrados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cargos = Cargo.objects.all()
        serializer = CargosCadastradosSerializer(cargos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NovoCargo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nome = request.data.get('nome')

        # Encontrar a instância de Registros_saida com base na descrição
        if Cargo.objects.filter(nome=nome).exists():
            return Response(
                {"error": "Cargo já está existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar um novo cargo
        try:
            novo_cargo = Cargo.objects.create(
                nome=nome
            )
            novo_cargo.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CargosCadastradosSerializer(novo_cargo)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListaFuncionariosCadastrados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        funcionarios = Funcionario.objects.all()
        serializer = FuncionariosCadastradosSerializer(funcionarios, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NovoFuncionario(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nome = request.data.get('nome')
        sobrenome = request.data.get('sobrenome')
        data_nascimento = request.data.get('data_nascimento')
        sexo = request.data.get('sexo')
        cargo_id = request.data.get('cargo_id')
        cpf = request.data.get('cpf')

        # Validar se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return Response(
                {"error": "CPF precisa ter exatamente 11 dígitos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Converter data do formato brasileiro para o formato ISO
        try:
            data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y')
        except ValueError:
            return Response(
                {"error": "Data de nascimento inválida. Use o formato dd/mm/yyyy."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Converter a data de nascimento para um datetime com fuso horário UTC
        data_nascimento = timezone.make_aware(data_nascimento)

        # Encontrar a instância de Aluno com base no CPF
        if Funcionario.objects.filter(cpf=cpf).exists():
            return Response(
                {"error": "CPF já está em uso."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar um novo aluno
        try:
            novo_funcionario = Funcionario.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                data_nascimento=data_nascimento,
                sexo=sexo,
                cargo_id=cargo_id,
                cpf=cpf
            )
            novo_funcionario.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serializar e retornar os dados do novo aluno
        serializer = FuncionariosCadastradosSerializer(novo_funcionario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FolhaPagamentosCadastrados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        folha = Folha_Pagamento.objects.all()
        serializer = FolhaPagamentoSerializer(folha, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NovoRegistroFolhaPagamento(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.get('data')
        valor = request.data.get('valor')
        funcionario_id = request.data.get('funcionario_id')
        try:
            data = datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            return Response(
                {"error": "Data de pagamento inválida. Use o formato dd/mm/yyyy."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Converter a data de nascimento para um datetime com fuso horário UTC
        data = timezone.make_aware(data)
        # Criar um novo Registro Folha
        try:
            novo_registro_folha = Folha_Pagamento.objects.create(
                data=data,
                valor=valor,
                funcionario_id=funcionario_id
            )
            novo_registro_folha.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FolhaPagamentoSerializer(novo_registro_folha)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListaUsuariosCadastrados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios = User.objects.all()
        serializer = UsuariosCadastradosSerializer(usuarios, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class NovoUsuario(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        lastname = request.data.get('lastname')
        email = request.data.get('email')
        login = request.data.get('login')
        is_manager = request.data.get('is_manager')
        cargo_id = request.data.get('cargo_id')
        password = request.data.get('password')

        # Verificar se o login já está em uso
        if User.objects.filter(login=login).exists():
            return Response(
                {"error": "Login já está em uso."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar um novo usuário
        try:
            novo_usuario = User(
                name=name,
                lastname=lastname,
                email=email,
                login=login,
                is_manager=is_manager,
                cargo_id=cargo_id
            )
            novo_usuario.set_password(password)  # Hashear a senha
            novo_usuario.save()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serializar e retornar os dados do novo usuário
        serializer = UsuariosCadastradosSerializer(novo_usuario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
