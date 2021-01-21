# Inset Flask app Here


from requests import get
from flask import Flask

from control.view import View
from control.control import UserControl, ItemControl, LixeiraControl
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JSON_SORT_KEYS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# CHANNEL ID thingspeak - 1246821
# READ KEY thingspeak   - PXT4EAHQ28DYIXAP
# WRITE KEY thingspeak  - 400WQ27M8AEH9KP6


@app.route('/')
@cross_origin()
def main():
    return View.success('Bem vindx ao web-service da Lixeira Inteligente')
# ===============================================================


@app.route('/create/user', methods=['POST'])
def create_user():
    return UserControl.create_user()


@app.route('/get/user', methods=['GET'])
def get_user():
    return UserControl.get_user()


@app.route('/login/user', methods=['POST'])
def login_user():
    print('Request recevied')
    return UserControl.login_user()


@app.route('/delete/user', methods=['DELETE'])
def delete_user():
    return UserControl.delete_user()


@app.route('/change/user', methods=['POST'])
def change_user():
    return UserControl.change_user()
# ===============================================================


@app.route('/create/item', methods=['POST'])
def create_item():
    return ItemControl.create_item()


@app.route('/get/item', methods=['GET'])
def get_item():
    return ItemControl.get_item()


@app.route('/get/item/full', methods=['GET'])
def get_full_item_list():
    return ItemControl.get_full_item_list()
# ===============================================================


@app.route('/create/lixeira', methods=['POST'])
def create_lixeira():
    return LixeiraControl.create_lixeira()


@app.route('/get/lixeira', methods=['GET'])
def get_lixeira():
    return LixeiraControl.get_lixeira()


@app.route('/get/lixeira/capacidade', methods=['GET'])
def get_lixeiera_capacidade():
    return LixeiraControl.get_lixeiera_capacidade()


@app.route('/update/lixeira/capacidade', methods=['UPDATE'])
def update_lixeiera_capacidade():
    return LixeiraControl.update_lixeiera_capacidade()
# ===============================================================


@app.route('/ts/feed', methods=['GET'])
def get_thingspeak_feed():
    url = 'https://api.thingspeak.com/channels/1246821/feeds.json'
    params = {'api_key': 'PXT4EAHQ28DYIXAP', 'results': 1}  # INSERT READ API KEY HERE
    timeout = None
    r = get(url, params=params, timeout=timeout)
    return r


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(threaded=True)
