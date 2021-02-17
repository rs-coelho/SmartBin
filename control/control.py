from control.view import View
from webargs.flaskparser import parser
from marshmallow import ValidationError
from flask import request
from jwt import decode, encode
from datetime import datetime, timedelta
from functools import wraps

from control.request_list import TOKEN_AUTH
from control.request_list import CREATE_USER, GET_USER, CHANGE_USER, LOGIN_USER, CREATE_ITEM, GET_ITEM
from control.request_list import UPDATE_LIXEIRA_CAPACIDADE, GET_LIXEIRA, CREATE_LIXEIRA
from model.model import ListaUsers, ListaItens, ListaLixeiras

SECRET_KEY = 'HP75db9wOKAjIn2Ki9ZmSizEk0r6iiQJ'


def token_verify(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = parser.parse(TOKEN_AUTH, request)

        if not token:
            return View.error(403, 'Missing Token')

        try:
            data = decode(token['token'], SECRET_KEY)

        except:
            return View.error(403, 'Invalid Token')

        return f(*args, **kwargs)

    return decorated


def token_verify_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = parser.parse(TOKEN_AUTH, request)

        if not token:
            return View.error(403, 'Missing Token')

        try:
            data = decode(token['token'], SECRET_KEY)
            if ListaUsers.get_user_type(data['id_user']) == 'AD':
                return f(*args, **kwargs)

        except:
            return View.error(403, 'Invalid Token')

        return False

    return decorated


class UserControl:
    @staticmethod
    def create_user():
        try:
            args = parser.parse(CREATE_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.create_user(args['nome'], args['email'], args['password'])
        if user == 0:
            return View.error(405, 'email already in use')
        result = {'id_user': user.id_user, 'nome': user.nome, 'email': user.email}
        return View.success(result)

    @staticmethod
    def get_user():
        try:
            args = parser.parse(GET_USER, request)
            print(args)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.get_user(args['id_user'])
        result = [{'id_user': rst.id_user, 'nome': rst.nome, 'email': rst.email} for rst in user]
        return View.success(result)

    @staticmethod
    def login_user():
        try:
            args = parser.parse(LOGIN_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.login_user(args['email'], args['password'])
        token = False
        if user:
            token = encode({'id_user': user.id_user, 'exp': datetime.utcnow() + timedelta(days=2)}, SECRET_KEY)
            # 60 sec for test, 15 days in app
        result = {'token': token, 'email': user.email}
        return View.success(result)

    @staticmethod
    def delete_user():
        try:
            args = parser.parse(GET_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.delete_user(args['id_user'])
        result = [{'id_user': rst[0]} for rst in user]
        return View.success(result)

    @staticmethod
    def change_user():
        try:
            args = parser.parse(CHANGE_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.change_user(args['id_user'], args['nome'], args['email'], args['password'],
                                      args['pontos'], args['tipo_user'])
        result = [{'id_user': rst[0]} for rst in user]
        return View.success(result)


class ItemControl:
    @staticmethod
    def create_item():
        try:
            args = parser.parse(CREATE_ITEM, request)
        except ValidationError as err:
            return View.error(400, str(err))
        item = ListaItens.create_item(args['nome'], args['material'], args['peso'], args['pontos'])
        result = {'id_item': item.id_item, 'nome': item.nome, 'material': item.material}
        return View.success(result)

    @staticmethod
    def get_item():
        try:
            args = parser.parse(GET_ITEM, request)
            print(args)
        except ValidationError as err:
            return View.error(400, str(err))
        item = ListaItens.get_item(args['id_item'])
        result = [{'id_item': rst.id_item, 'nome': rst.nome, 'material': rst.material} for rst in item]
        return View.success(result)

    @staticmethod
    def get_full_item_list():
        try:
            item = ListaItens.get_full_item_list()
        except ValidationError as err:
            return View.error(400, str(err))

        result = [{'id_item': rst.id_item, 'nome': rst.nome, 'material': rst.material} for rst in item]
        return View.success(result)


class LixeiraControl:
    @staticmethod
    def create_lixeira():
        try:
            args = parser.parse(CREATE_LIXEIRA, request)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.create_lixeira(args['enderesso_fisico'], args['capacidade'], args['status'])
        result = {'id_lixeira': lixeira.id_lixeira, 'enderesso_fisico': lixeira.enderesso_fisico, 'capacidade': lixeira.capacidade}
        return View.success(result)

    @staticmethod
    def get_lixeira():
        try:
            args = parser.parse(GET_LIXEIRA, request)
            print(args)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.get_lixeira(args['id_lixeira'])
        result = {'id_lixeira': lixeira[0].id_lixeira, 'enderesso_fisico': lixeira[0].enderesso_fisico}
        return View.success(result)

    @staticmethod
    def get_lixeiera_capacidade():
        try:
            args = parser.parse(GET_LIXEIRA, request)
            print(args)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.get_lixeiera_capacidade(args['id_lixeira'])
        result = {'id_lixeira': lixeira[0].id_lixeira, 'capacidade': lixeira[0].capacidade}
        return View.success(result)

    @staticmethod
    def update_lixeiera_capacidade():
        try:
            args = parser.parse(UPDATE_LIXEIRA_CAPACIDADE, request)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.update_lixeiera_capacidade(args['id_lixeira'], args['capacidade'])
        result = {'id_lixeira': lixeira[0].id_lixeira, 'capacidade': lixeira[0].capacidade}
        return View.success(result)
