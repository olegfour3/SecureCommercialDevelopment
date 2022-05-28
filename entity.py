from config import host_db, port_db, user_db, password_db, db_name
import psycopg2

postgresql_error_sample = "[INFO] Error while working with PostgreSQL:\n"


def connect_to_db():
    try:
        # connect to database
        connection = psycopg2.connect(
            host=host_db,
            port=port_db,
            database=db_name,
            user=user_db,
            password=password_db
        )
        # connection.autocommit = True
        print("[INFO] Connection to PostgreSQL successful")

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


def db_request(request_text: str, return_all=True):
    try:
        connection = connect_to_db()
        # connection.autocommit = True

        if connection is None:
            return None
        # the cursor for performing database operations
        with connection.cursor() as cursor:
            cursor.execute(
                request_text
            )
            # cursor = connection.cursor()
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
            print("[INFO] PostgreSQL connection closed")
        return data


