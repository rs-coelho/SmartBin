from flask import Flask
from flasgger import Swagger

from control.view import View
from control.control import UserControl, ItemControl, BinControl, SECRET_KEY
from control.control import token_verify_admin_or_bin, token_verify_admin, token_verify
from control.control import InventoryControl
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
cors = CORS(app)
bcrypt = Bcrypt(app)

app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 3}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger = Swagger(app, config=swagger_config)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JSON_SORT_KEYS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
@cross_origin()
def main():
    return View.success('Welcome to the Smart Bins web-service!')

# ===============================================================
# ===============           User List      ======================


@app.route('/create/user', methods=['POST'])  # ok
def create_user():
    return UserControl.create_user()


@app.route('/get/user', methods=['GET'])  # ok
@token_verify
def get_user():
    return UserControl.get_user()


@app.route('/login/user', methods=['POST'])  # ok
def login_user():
    """
        file: route_docs/login_user.yml
    """
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
# ===============           Inventory      ======================


@app.route('/insert/item/inventory', methods=['POST'])  # ok
@token_verify
def insert_item_from_user():
    return InventoryControl.insert_item_from_user()


@app.route('/get/user/inventory', methods=['GET'])  # ok
@token_verify
def get_items_from_user():
    return InventoryControl.get_items_from_user()


@app.route('/empty/bin', methods=['POST'])  # works but needs ajusts
@token_verify
def empty_trash():
    return InventoryControl.empty_trash()

# ===============================================================
# ===============           Bin List       ======================


@app.route('/create/bin', methods=['POST'])  # Admin ok
@token_verify_admin
def create_bin():
    return BinControl.create_bin()


@app.route('/get/bin', methods=['GET'])  # ok
@token_verify
def get_bin():
    return BinControl.get_bin()


@app.route('/get/bin/capacity', methods=['GET'])  # ok
@token_verify
def get_bin_capacity():
    return BinControl.get_bin_capacity()


@app.route('/update/bin/capacity', methods=['POST'])  # Admin ok
@token_verify_admin  # later change to admin_or_bin
def update_bin_capacity():
    return BinControl.update_bin_capacity()
# ===============================================================


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(threaded=True)
