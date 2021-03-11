from flask import Flask

from control.view import View
from control.control import UserControl, ItemControl, LixeiraControl, SECRET_KEY
from control.control import token_verify_admin_or_lixeira, token_verify_admin, token_verify
from control.control import InventarioControl
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
# ===============           User List      ======================


@app.route('/create/user', methods=['POST'])  # ok
def create_user():
    return UserControl.create_user()


@app.route('/get/user', methods=['GET'])  # ok
@token_verify
def get_user():
    return UserControl.get_user()


@app.route('/login/user', methods=['GET'])  # ok
def login_user():
    return UserControl.login_user()


@app.route('/delete/user', methods=['DELETE'])  # needs adjusts
@token_verify
def delete_user():  # First delete inventory then the user,
    # alert the user that they will lose all their records
    return UserControl.delete_user()


@app.route('/change/user', methods=['POST'])  # needs adjusts
@token_verify
def change_user():
    return UserControl.change_user()
# ===============================================================
# ===============           Item List      ======================


@app.route('/create/item', methods=['POST'])  # Admin ok
@token_verify_admin
def create_item():
    return ItemControl.create_item()


@app.route('/get/item', methods=['GET'])  # ok
@token_verify
def get_item():
    return ItemControl.get_item()


@app.route('/post/item/img', methods=['POST'])  # needs adjusts route and request ok, but DB does not save the img
@token_verify_admin
def upload_item_img():
    return ItemControl.upload_item_img()


@app.route('/get/item/full', methods=['GET'])  # ok
@token_verify
def get_full_item_list():
    return ItemControl.get_full_item_list()
# ===============================================================
# ===============           Invertory      ======================


@app.route('/insert/item/inventory', methods=['POST'])  # ok
@token_verify
def insert_item_from_user():
    return InventarioControl.insert_item_from_user()


@app.route('/get/user/inventory', methods=['GET'])  # ok
@token_verify
def get_items_from_user():
    return InventarioControl.get_items_from_user()


@app.route('/empty/lixeira', methods=['POST'])  # works but needs ajusts
@token_verify
def empty_trash():
    return InventarioControl.empty_trash()
# ===============================================================
# ===============           Bin List       ======================


@app.route('/create/lixeira', methods=['POST'])  # Admin ok
@token_verify_admin
def create_lixeira():
    return LixeiraControl.create_lixeira()


@app.route('/get/lixeira', methods=['GET'])  # ok
@token_verify
def get_lixeira():
    return LixeiraControl.get_lixeira()


@app.route('/get/lixeira/capacidade', methods=['GET'])  # ok
@token_verify
def get_lixeiera_capacidade():
    return LixeiraControl.get_lixeira_capacidade()


@app.route('/update/lixeira/capacidade', methods=['POST'])  # Admin ok
@token_verify_admin_or_lixeira
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
