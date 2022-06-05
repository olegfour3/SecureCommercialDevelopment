from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
import psycopg2

postgresql_error_sample = "[ERR] Error while working with PostgreSQL:\n"


def connect_to_db():
    try:
        # connect to database
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        # connection.autocommit = True

    except Exception as _ex:
        print(postgresql_error_sample, _ex)
        return None

    return connection


def test_connect_to_db():
    connection = connect_to_db()
    if connection is None:
        return False
    else:
        # the cursor for performing database operations
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f'Server version: {cursor.fetchone()}')
        connection.close()
        print("[INFO] PostgreSQL connection closed")
        return True


def request(request_text: str, return_all=True):
    data = []
    try:
        connection = connect_to_db()

        if connection is None:
            return None

        with connection.cursor() as cursor:
            cursor.execute(
                request_text
            )
            if return_all:
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()

    except Exception as _ex:
        print(postgresql_error_sample, _ex)
        return None
    finally:
        # close connection
        if connection:
            connection.close()
        return data


def insert_delete(delete_text: str):
    data = [False, '']
    try:
        connection = connect_to_db()
        connection.autocommit = True

        if connection is None:
            return False
        # the cursor for performing database operations
        with connection.cursor() as cursor:
            cursor.execute(
                delete_text
            )
        data = [True, 'Операция успешно завершена']

    except Exception as _ex:
        print(postgresql_error_sample, _ex)
        data = [False, 'Ошибка при опреции :c\nОбратитесь к администратору!']
    finally:
        # close connection
        if connection:
            connection.close()
        return data