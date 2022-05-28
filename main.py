from flask import request, Flask
import crypt_controller
from entity import test_connect_to_db

# starting the app
app = Flask("Safe Enterprise Development")
if not test_connect_to_db():
    print("[INFO] App stopped")
    exit()
print("[INFO] App run successful")


@app.route('/decode', methods=['POST'])
def decode():
    request_data = request.get_json()
    data_text = crypt_controller.decode(request_data["key"], request_data["data"])
    return data_text


@app.route('/encode', methods=['POST'])
def encode():
    request_data = request.get_json()
    data_text = crypt_controller.encode(request_data["key"], request_data["data"])
    return data_text



