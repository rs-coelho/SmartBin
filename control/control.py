from control.view import View
from webargs.flaskparser import parser
from marshmallow import ValidationError
from flask import request

from control.request_list import CREATE_USER, GET_USER, CHANGE_USER,LOGIN_USER, CREATE_ITEM, GET_ITEM
from model.model import ListaUsers, ListaItens


class UserControl:
    @staticmethod
    def create_user():
        try:
            args = parser.parse(CREATE_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.create_user(args['nome'], args['email'], args['password'], args['pontos'], args['tipo_user'])
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
            print(args)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.login_user(args['email'],args['password'])
        result = [{'id_user': rst.id_user, 'email': rst.email} for rst in user]
        return View.success(result)

    @staticmethod
    def delete_user():
        try:
            args = parser.parse(GET_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.delete_user(GET_USER)
        result = [{'id_user': rst[0]} for rst in user]
        return View.success(result)

    @staticmethod
    def change_user():
        try:
            args = parser.parse(CHANGE_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        user = ListaUsers.change_user(CHANGE_USER)
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
