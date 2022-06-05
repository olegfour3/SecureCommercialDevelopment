import threading
from db_entity import test_connect_to_db
from api_service import start_api_service
from telegram_bot import start_bot


if __name__ == "__main__":
    api_thread = threading.Thread(target=start_api_service)
    try:
        test_connect_to_db()
        api_thread.start()
        start_bot()
    except Exception as _ex:
        print('[ERR] App launch error:\n', _ex)
        exit()




