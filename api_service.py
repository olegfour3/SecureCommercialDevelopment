from flask import request, Flask
import crypt_controller

if __name__ == '__main__':
    try:
        app = Flask("Safe Enterprise Development")
        print('[INFO] API launched')
    except Exception as _ex:
        print('[ERR] API startup error:\n', _ex)
else:
    app = Flask("Safe Enterprise Development")


def start_api_service():
    try:
        print('[INFO] API launched')
        app.run()
    except Exception as _ex:
        print('[ERR] API startup error:\n', _ex)


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


