from django.urls import path

from .views import (AlunosCadastrados, EditarEntrada, ExcluirEntrada,
                    ExcluirSaida, FolhaPagamentosCadastrados,
                    ListaCargosCadastrados, ListaEntradas,
                    ListaEntradasCadastradas, ListaFuncionariosCadastrados,
                    ListaMatriculasCadastradas, ListaSaidas,
                    ListaSaidasCadastradas, ListaUsuariosCadastrados,
                    NovaEntrada, NovaSaida, NovoAluno, NovoCargo,
                    NovoFuncionario, NovoRegistroFolhaPagamento,
                    NovoTipoEntrada, NovoTipoMatricula, NovoTipoRecebimento,
                    NovoTipoSaida, NovoUsuario, RecebimentosCadastrados)

urlpatterns = [
    # Entradas
    path('entradas-cadastradas/', ListaEntradasCadastradas.as_view(), name='lista_entradas_cadastradas'),
    path('entradas-cadastradas/nova/', NovoTipoEntrada.as_view(), name='cadastrar_novo_tipo_entrada'),
    path('entrada/nova/', NovaEntrada.as_view(), name='nova_entrada'),
    path('entradas/', ListaEntradas.as_view(), name='lista_entradas'),
    path('entradas/<int:entrada_id>/editar/', EditarEntrada.as_view(), name='editar_entrada'),
    path('entradas/<int:entrada_id>/excluir/', ExcluirEntrada.as_view(), name='excluir_entrada'),

    # Saídas
    path('saidas-cadastradas/', ListaSaidasCadastradas.as_view(), name='lista_saidas_cadastradas'),
    path('saidas-cadastradas/nova/', NovoTipoSaida.as_view(), name='cadastrar_novo_tipo_saida'),
    path('saidas/', ListaSaidas.as_view(), name='lista_saidas'),
    path('saida/nova/', NovaSaida.as_view(), name='nova_saida'),
    path('saidas/<int:saida_id>/excluir/', ExcluirSaida.as_view(), name='excluir_entrada'),

    # Tipo_Matricula
    path('tipos-matriculas-cadastradas/', ListaMatriculasCadastradas.as_view(), name='lista_tipos_matriculas_cadastradas'),
    path('tipos-matriculas/nova/', NovoTipoMatricula.as_view(), name='nova_matricula'),

    # Alunos
    path('alunos/', AlunosCadastrados.as_view(), name='lista_tipos_matriculas_cadastradas'),
    path('alunos/novo/', NovoAluno.as_view(), name='nova_matricula'),

    # Recebimentos
    path('recebimentos/', RecebimentosCadastrados.as_view(), name='lista_tipos_recebimentos'),
    path('recebimentos/novo/', NovoTipoRecebimento.as_view(), name='cadastrar_novo_tipo_entrada'),

    # Cargos
    path('cargos/', ListaCargosCadastrados.as_view(), name='lista_cargos'),
    path('cargos/novo/', NovoCargo.as_view(), name='novo_cargo'),

    # Funcionários
    path('funcionarios/', ListaFuncionariosCadastrados.as_view(), name='list_funcionarios'),
    path('funcionarios/novo/', NovoFuncionario.as_view(), name='novo_funcionario'),

    # Folha de pagamentos
    path('folha-pagamentos/', FolhaPagamentosCadastrados.as_view(), name='list_funcionarios'),
    path('folha-pagamentos/novo/', NovoRegistroFolhaPagamento.as_view(), name='novo_funcionario'),

    # Usuários
    path('usuarios/', ListaUsuariosCadastrados.as_view(), name='list_funcionarios'),
    path('usuarios/novo/', NovoUsuario.as_view(), name='novo_funcionario'),


]
