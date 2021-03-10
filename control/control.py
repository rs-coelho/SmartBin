import configparser, os
from webargs.flaskparser import parser
from marshmallow import ValidationError
from flask import request
from jwt import decode, encode
from datetime import datetime, timedelta
from functools import wraps

from control.view import View
from control.request_list import CREATE_USER, GET_USER, CHANGE_USER, LOGIN_USER, CREATE_ITEM, GET_ITEM, UPLOAD_ITEM_IMG
from control.request_list import UPDATE_LIXEIRA_CAPACIDADE, GET_LIXEIRA, CREATE_LIXEIRA
from control.request_list import CREATE_INV_ITEM
from model.model import ListaUsers, ListaItens, ListaLixeiras, InventarioItens

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../settings/settings.ini'))

SECRET_KEY = config.get('SECRET', 'key')


def token_verify(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = parser.parse(TOKEN_AUTH, request)
        token = request.headers

        if not token:
            return View.error(401, 'Missing Token')

        try:
            data = decode(token['Authorization'], SECRET_KEY, algorithms='HS256')

        except:
            return View.error(401, 'Invalid Token')

        return f(*args, **kwargs)

    return decorated


def token_verify_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = parser.parse(TOKEN_AUTH, request)
        token = request.headers

        if not token:
            return View.error(401, 'Missing Token')

        data = decode(token['Authorization'], SECRET_KEY, algorithms='HS256')
        if ListaUsers.get_user_type(data['id_user']) == 'AD':
            return f(*args, **kwargs)

        return View.error(401, 'Invalid Token')

    return decorated


def token_verify_admin_or_lixeira(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = parser.parse(TOKEN_AUTH, request)
        token = request.headers

        if not token:
            return View.error(401, 'Missing Token')

        data = decode(token['Authorization'], SECRET_KEY, algorithms='HS256')
        if ListaUsers.get_user_type(data['id_user']) in ('AD', 'LX'):
            return f(*args, **kwargs)

        return View.error(401, 'Invalid Token')

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
            token = encode({'id_user': user.id_user, 'exp': datetime.utcnow() + timedelta(days=15)}, SECRET_KEY)
        else:
            return View.error(401, 'Access Denied, wrong authenticators')
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
        result = [{'id_item': rst.id_item, 'nome': rst.nome, 'material': rst.material, 'img_base64': rst.img_base64}
                  for rst in item]
        return View.success(result)

    @staticmethod
    def upload_item_img():
        try:
            args = parser.parse(UPLOAD_ITEM_IMG, request)
        except ValidationError as err:
            return View.error(400, str(err))
        item = ListaItens.upload_item_img(args['id_item'], args['img_base64'])
        result = {'id_item': item.id_item, 'img_base64': item.img_base64}
        return View.success(result)

    @staticmethod
    def get_full_item_list():
        try:
            item = ListaItens.get_full_item_list()
        except ValidationError as err:
            return View.error(400, str(err))

        result = [{'id_item': rst.id_item, 'nome': rst.nome, 'material': rst.material, 'img_base64': rst.img_base64}
                  for rst in item]
        return View.success(result)


class InventarioControl:
    @staticmethod
    def insert_item_from_user():
        try:
            args = parser.parse(CREATE_INV_ITEM, request)
        except ValidationError as err:
            return View.error(400, str(err))
        item = InventarioItens.insert_item_from_user(args['id_user'], args['id_lixeira'], args['id_item'])
        result = {'id_user': item.id_user, 'id_lixeira': item.id_lixeira, 'id_item': item.id_item}
        return View.success(result)

    @staticmethod
    def get_items_from_user():
        try:
            args = parser.parse(GET_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        item = InventarioItens.get_items_from_user(args['id_user'])
        result = [{'id_item': rst.id_item, 'id_lixeira': rst.id_lixeira} for rst in item]
        return View.success(result)

    @staticmethod
    def empty_trash():
        try:
            args = parser.parse(GET_LIXEIRA, request)
            print(args, 'This bin should be empty')
        except ValidationError as err:
            return View.error(400, str(err))
        item = InventarioItens.empty_trash(args['id_lixeira'])
        result = [{'id_item': rst.id_item, 'id_lixeira': rst.id_lixeira} for rst in item]
        return View.success(result)


class LixeiraControl:
    @staticmethod
    def create_lixeira():
        try:
            args = parser.parse(CREATE_LIXEIRA, request)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.create_lixeira(args['address'], args['capacity'], args['status'])
        result = {'id_lixeira': lixeira.id_lixeira, 'address': lixeira.address, 'capacity': lixeira.capacity}
        return View.success(result)

    @staticmethod
    def get_lixeira():
        try:
            args = parser.parse(GET_LIXEIRA, request)
            print(args)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.get_lixeira(args['id_lixeira'])
        if not lixeira:
            return View.error(404, 'Bin not found')
        result = {'id_lixeira': lixeira[0].id_lixeira, 'address': lixeira[0].address}
        return View.success(result)

    @staticmethod
    def get_lixeira_capacidade():
        try:
            args = parser.parse(GET_LIXEIRA, request)
            print(args)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.get_lixeira(args['id_lixeira'])
        result = {'id_lixeira': lixeira[0].id_lixeira, 'capacity': lixeira[0].capacity}
        return View.success(result)

    @staticmethod
    def update_lixeiera_capacidade():
        try:
            args = parser.parse(UPDATE_LIXEIRA_CAPACIDADE, request)
        except ValidationError as err:
            return View.error(400, str(err))
        lixeira = ListaLixeiras.update_lixeiera_capacidade(args['id_lixeira'], args['capacity'])
        result = {'id_lixeira': lixeira[0].id_lixeira, 'capacity': lixeira[0].capacity, 'last_updated': lixeira[0].last_updated}
        return View.success(result)
