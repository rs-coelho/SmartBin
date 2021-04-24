import configparser
import os
from webargs.flaskparser import parser
from marshmallow import ValidationError
from flask import request
from jwt import decode, encode
from datetime import datetime, timedelta
from functools import wraps

from control.view import View
from control.request_list import CREATE_USER, CHANGE_USER, LOGIN_USER, CREATE_ITEM, UPLOAD_ITEM_IMG
from control.request_list import UPDATE_BIN_CAPACITY, GET_BIN, CREATE_BIN
from control.request_list import CREATE_INV_ITEM
from model.model import ListUsers, ListItems, ListBins, InventoryItems

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
        if ListUsers.get_user_type(data['id_user']) == 'AD':
            return f(*args, **kwargs)

        return View.error(401, 'Invalid Token')

    return decorated


def token_verify_admin_or_bin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = parser.parse(TOKEN_AUTH, request)
        token = request.headers

        if not token:
            return View.error(401, 'Missing Token')

        data = decode(token['Authorization'], SECRET_KEY, algorithms='HS256')
        if ListUsers.get_user_type(data['id_user']) in ('AD', 'LX'):
            return f(*args, **kwargs)

        return View.error(401, 'Invalid Token')

    return decorated


class UserControl:
    @staticmethod
    def create_user():
        try:
            args = parser.parse(CREATE_USER, request)
            user = ListUsers.create_user(args['name'], args['email'], args['password'])
            if user == 0:
                return View.error(405, 'email already in use')

            result = {'id_user': user.id_user, 'name': user.name, 'email': user.email}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def get_user():
        try:
            user = ListUsers.get_user(decode(request.headers['Authorization'],
                                             SECRET_KEY, algorithms='HS256')['id_user'])

            result = [{'id_user': rst.id_user, 'name': rst.name, 'email': rst.email, 'points': rst.points} for rst in
                      user]
        except ValidationError as err:
            return View.error(400, str(err))

        return View.success(result)

    @staticmethod
    def login_user():
        try:
            args = parser.parse(LOGIN_USER, request)
            user = ListUsers.login_user(args['email'], args['password'])
            if user:
                token = encode({'id_user': user.id_user, 'exp': datetime.utcnow() + timedelta(days=15)}, SECRET_KEY)
            else:
                return View.error(401, 'Access Denied, wrong authenticators')

            result = {'token': token, 'email': user.email}
        except ValidationError as err:
            return View.error(400, str(err))

        return View.success(result)

    @staticmethod
    def delete_user():
        try:
            user = ListUsers.delete_user(decode(request.headers['Authorization'],
                                                SECRET_KEY, algorithms='HS256')['id_user'])
            if user:
                return View.success('User Deleted')
            else:
                return View.error(404, 'User Not Found')
        except ValidationError as err:
            return View.error(400, str(err))

    @staticmethod
    def change_user():
        try:
            args = parser.parse(CHANGE_USER, request)
            user = ListUsers.change_user(decode(request.headers['Authorization'],
                                                SECRET_KEY, algorithms='HS256')['id_user'], args)

            result = {'id_user': user.id_user}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)


class ItemControl:
    @staticmethod
    def create_item():
        try:
            args = parser.parse(CREATE_ITEM, request)
            item = ListItems.create_item(args['id_item'], args['name'], args['material'], args['weight'],
                                         args['points'])

            result = {'id_item': item.id_item, 'name': item.name, 'material': item.material}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def get_item(id_item):
        try:
            rst = ListItems.get_item(id_item)

            result = {'id_item': rst.id_item, 'name': rst.name, 'material': rst.material, 'points': rst.points,
                      'img_base64': rst.img_base64}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def upload_item_img():
        try:
            args = parser.parse(UPLOAD_ITEM_IMG, request)
            item = ListItems.upload_item_img(args['id_item'], args['img_base64'])

            result = {'id_item': item.id_item, 'img_base64': item.img_base64}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def get_full_item_list():
        try:
            item = ListItems.get_full_item_list()

            result = [{'id_item': rst.id_item, 'name': rst.name, 'material': rst.material, 'points': rst.points,
                       'img_base64': rst.img_base64} for rst in item]
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)


class InventoryControl:
    @staticmethod
    def insert_item_from_user():
        try:
            args = parser.parse(CREATE_INV_ITEM, request)
            id_user = decode(request.headers['Authorization'], SECRET_KEY, algorithms='HS256')['id_user']
            if args['id_item'] not in ListItems.get_full_item_list():
                return View.error(404, 'Item not found in')
            item = InventoryItems.insert_item_from_user(id_user, args['id_bin'], args['id_item'])
            prox_item = ListItems.get_item(args['id_item'])
            ListUsers.update_user_points(id_user, prox_item.points)

            result = {'id_user': item.id_user, 'id_bin': item.id_bin, 'id_item': item.id_item}
        except ValidationError as err:
            return View.error(400, str(err))

        return View.success(result)

    @staticmethod
    def get_items_from_user():
        try:
            items = InventoryItems.get_items_from_user(decode(request.headers['Authorization'],
                                                              SECRET_KEY, algorithms='HS256')['id_user'])
            id_list = []
            [id_list.append(x.id_item) for x in items]
            full_list = ListItems.get_item_list(id_list)
            qtd_list = {item: full_list.count(item) for item in full_list}

            result = [{'id_item': rst.id_item, 'name': rst.name, 'material': rst.material, 'points': rst.points,
                       'img_base64': rst.img_base64, 'quantity': qtd_list[rst]} for rst in qtd_list.keys()]

        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def empty_trash():
        try:
            args = parser.parse(GET_BIN, request)
            item = InventoryItems.empty_trash(args['id_bin'])

            result = [{'id_item': rst.id_item, 'id_bin': rst.id_bin} for rst in item]
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)


class BinControl:
    @staticmethod
    def create_bin():
        try:
            args = parser.parse(CREATE_BIN, request)
            rec_bin = ListBins.create_bin(args['address'], args['capacity'], args['status'])

            result = {'id_bin': rec_bin.id_bin, 'address': rec_bin.address, 'capacity': rec_bin.capacity}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def get_bin():
        try:
            args = parser.parse(GET_BIN, request)
            rec_bin = ListBins.get_bin(args['id_bin'])
            if not rec_bin:
                return View.error(404, 'Bin not found')

            result = {'id_bin': rec_bin[0].id_bin, 'address': rec_bin[0].address}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def get_bin_capacity():
        try:
            args = parser.parse(GET_BIN, request)
            rec_bin = ListBins.get_bin(args['id_bin'])

            result = {'id_bin': rec_bin[0].id_bin, 'capacity': rec_bin[0].capacity}
        except ValidationError as err:
            return View.error(400, str(err))
        return View.success(result)

    @staticmethod
    def update_bin_capacity():
        try:
            args = parser.parse(UPDATE_BIN_CAPACITY, request)
            rec_bin = ListBins.update_bin_capacity(args['id_bin'], args['capacity'])

            result = {'id_bin': rec_bin[0].id_bin, 'capacity': rec_bin[0].capacity,
                      'last_updated': rec_bin[0].last_updated}
        except ValidationError as err:
            return View.error(400, str(err))

        return View.success(result)
