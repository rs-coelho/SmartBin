# Inset Flask app Here


from flask import Flask
from control.view import View
from control.control import UserControl


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def main():
    return View.success('Bem vindx ao web-service da Lixeira Inteligente')


@app.route('/create/user', methods=['POST'])
def create_user():
    return View.error(404,'Função indisponivel')


@app.route('/get/user', methods=['GET'])
def get_user():
    return UserControl.get_user()


@app.route('/delete/user', methods=['DELETE'])
def delete_user():
    return View.error(404,'Função indisponivel')


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(threaded=True)
