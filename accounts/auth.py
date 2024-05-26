from accounts.models import Cargo, User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.exceptions import APIException, AuthenticationFailed


class Authentication:
    def signin(self, login=None, password=None) -> User:
        exception_auth = AuthenticationFailed('Login e/ou senha incorreto(s)')

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            raise exception_auth

        if not check_password(password, user.password):
            raise exception_auth

        return user

    def signup(self, name, login, password, email, lastname, cargo="Recepcionista", is_manager=False):
        if not name or name == '':
            raise APIException('O nome não deve ser null')

        if not lastname or lastname == '':
            raise APIException('O sobrenome não deve ser null')

        if not login or login == '':
            raise APIException('O login não deve ser vazio')

        if not email or email == '':
            raise APIException('O email não deve ser vazio')

        if not password or password == '':
            raise APIException('O password não deve ser null')

        try:
            cargo_obj = Cargo.objects.get(nome=cargo)
        except Cargo.DoesNotExist:
            raise APIException('O cargo fornecido é inválido')

        if User.objects.filter(login=login).exists():
            raise APIException('Este login já possui cadastro na plataforma')

        # Criação do hash da senha
        password_hashed = make_password(password)

        # Criar o usuário
        created_user = User.objects.create(
            name=name,
            lastname=lastname,
            cargo=cargo_obj,  # Usar o objeto Cargo encontrado
            login=login,
            email=email,
            is_manager=is_manager,
            password=password_hashed,
        )

        return created_user
