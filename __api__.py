# Inset Flask app Here

from flask import Flask

from control.view import View
from control.control import UserControl, ItemControl, LixeiraControl, SECRET_KEY, token_verify
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
cors = CORS(app)
bcrypt = Bcrypt(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JSON_SORT_KEYS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
@cross_origin()
def main():
    return View.success('Bem vindx ao web-service da Lixeira Inteligente')
# ===============================================================


@app.route('/create/user', methods=['POST'])
def create_user():
    return UserControl.create_user()


@app.route('/get/user', methods=['GET'])
@token_verify
def get_user():
    return UserControl.get_user()


@app.route('/login/user', methods=['POST'])
def login_user():
    return UserControl.login_user()


@app.route('/delete/user', methods=['DELETE'])
@token_verify
def delete_user():  # First delete inventory then the user,
    # alert the user that they will lose all their records
    return UserControl.delete_user()


@app.route('/change/user', methods=['POST'])
@token_verify
def change_user():
    return UserControl.change_user()
# ===============================================================

# Create a token Verify Admin


@app.route('/create/item', methods=['POST'])  # Admin
def create_item():
    return ItemControl.create_item()


@app.route('/get/item', methods=['GET'])
@token_verify
def get_item():
    return ItemControl.get_item()


@app.route('/get/item/full', methods=['GET'])
@token_verify
def get_full_item_list():
    return ItemControl.get_full_item_list()
# ===============================================================


@app.route('/create/lixeira', methods=['POST'])  # Admin
def create_lixeira():
    return LixeiraControl.create_lixeira()


@app.route('/get/lixeira', methods=['GET'])
@token_verify
def get_lixeira():
    return LixeiraControl.get_lixeira()


@app.route('/get/lixeira/capacidade', methods=['GET'])
@token_verify
def get_lixeiera_capacidade():
    return LixeiraControl.get_lixeiera_capacidade()


@app.route('/update/lixeira/capacidade', methods=['POST'])  # Admin
def update_lixeiera_capacidade():
    return LixeiraControl.update_lixeiera_capacidade()
# ===============================================================


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(threaded=True)
