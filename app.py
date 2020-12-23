# Inset Flask app Here


from requests import get
from flask import Flask, jsonify

from control.view import View
from control.control import UserControl


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# CHANNEL ID thingspeak - 1246821
# READ KEY thingspeak   - PXT4EAHQ28DYIXAP
# WRITE KEY thingspeak  - 400WQ27M8AEH9KP6


@app.route('/')
def main():
    return View.success('Bem vindx ao web-service da Lixeira Inteligente')


@app.route('/create/user', methods=['POST'])
def create_user():
    return UserControl.create_user()


@app.route('/get/user', methods=['GET'])
def get_user():
    print('Request recevied')
    return UserControl.get_user()


@app.route('/delete/user', methods=['DELETE'])
def delete_user():
    return UserControl.delete_user()


@app.route('/change/user', methods=['POST'])
def change_user():
    return UserControl.change_user()


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
