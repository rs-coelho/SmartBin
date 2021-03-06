from flask import jsonify
from collections import OrderedDict


class View(object):

    @staticmethod
    def success_without_data():
        result = OrderedDict()
        result['success'] = 'true'
        result['payload'] = OrderedDict()
        result['payload']['code'] = 200
        result['payload']['message'] = 'SUCCESS'
        return jsonify(result)

    @staticmethod
    def success_with_message(message):
        result = OrderedDict()
        result['success'] = 'true'
        result['payload'] = OrderedDict()
        result['payload']['code'] = 200
        result['payload']['message'] = message
        return jsonify(result)

    @staticmethod
    def success(data):
        result = OrderedDict()
        result['success'] = 'true'
        result['payload'] = OrderedDict()
        result['payload']['code'] = 200
        result['payload']['message'] = 'SUCCESS'
        result['payload']['data'] = data
        return jsonify(result)

    @staticmethod
    def accepted():
        result = OrderedDict()
        result['success'] = 'true'
        result['payload'] = OrderedDict()
        result['payload']['code'] = 202
        result['payload']['message'] = 'ACCEPTED'
        return jsonify(result)

    @staticmethod
    def error(code, details, success=True):
        messages = {400: 'Bad request', 401: 'Token Problems', 404: 'Not found', 405: 'Not allowed', 409: 'Conflict', 500: 'Internal error'}
        result = OrderedDict()
        result['success'] = success
        result['payload'] = OrderedDict()
        result['payload']['error'] = OrderedDict()
        result['payload']['error']['code'] = code
        result['payload']['error']['message'] = messages[code]
        result['payload']['error']['details'] = details
        return jsonify(result)

    @staticmethod
    def authorization_error():
        result = OrderedDict()
        result['error'] = 'access_denied'
        result['error_description'] = 'The resource owner or authorization server denied the request.'
        return jsonify(result)
