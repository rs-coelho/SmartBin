from flask import jsonify
from collections import OrderedDict


class View(object):

    @staticmethod
    def success_with_message(message):
        result = OrderedDict()
        result['connected'] = 'true'
        result['message'] = message
        return jsonify(result), 200

    @staticmethod
    def success(data):
        result = OrderedDict()
        result['connected'] = 'true'
        result['data'] = data
        return jsonify(result), 200

    @staticmethod
    def accepted():
        result = OrderedDict()
        result['connected'] = 'true'
        result['message'] = 'ACCEPTED'
        return jsonify(result), 202

    @staticmethod
    def error(code, details):
        messages = {400: 'Bad request', 401: 'Authorization Problems', 404: 'Not found', 405: 'Not allowed',
                    409: 'Conflict', 500: 'Internal error'}
        result = OrderedDict()
        result['connected'] = 'true'
        result['error'] = OrderedDict()
        result['error']['message'] = messages[code]
        result['error']['details'] = details
        return jsonify(result), code

    @staticmethod
    def authorization_error():
        result = OrderedDict()
        result['error'] = 'access_denied'
        result['error_description'] = 'The resource owner or authorization server denied the request.'
        return jsonify(result)
