from control.view import View
from webargs.flaskparser import parser
from marshmallow import ValidationError
from flask import request

from control.request_list import GET_USER
from model.model import ListaUsers


class UserControl:
    @staticmethod
    def get_user():
        try:
            args = parser.parse(GET_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        # implement get_user
        user = ListaUsers.get_user(GET_USER)
        result = [{'id_user': rst[0]} for rst in user]
        return View.success(result)

    @staticmethod
    def delete_user():
        try:
            args = parser.parse(GET_USER, request)
        except ValidationError as err:
            return View.error(400, str(err))
        # implement get_user
        user = ListaUsers.delete_user(GET_USER)
        result = [{'id_user': rst[0]} for rst in user]
        return View.success(result)



