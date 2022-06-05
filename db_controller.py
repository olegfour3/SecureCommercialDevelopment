import db_entity
from cryptography.fernet import Fernet


# CODE


def get_code(name_id: str):
    return db_entity.request(f"SELECT code FROM t_code WHERE name_id = {name_id};", False)


def get_client_subscription(subscription_serial_key: str):
    return db_entity.request(f"SELECT * FROM t_clients_subscription "
                             f"INNER JOIN t_clients ON t_clients_subscription.client_id = t_clients.id"
                             f"WHERE t_clients_subscription.serial_key = {subscription_serial_key}"
                             f"ORDER BY t_clients_subscription.validity_date DESC;", False)


# CLIENTS


def client_already_exist_by_id(client_id: str):
    res = db_entity.request("SELECT id FROM b_b.t_clients WHERE id = %s;" % (client_id))
    if len(res) == 0:
        return False
    else:
        return True


def client_already_exist_by_name(client_name: str):
    res = db_entity.request("SELECT name FROM b_b.t_clients WHERE name = '%s';" % (client_name))
    if len(res) == 0:
        return False
    else:
        return True


def get_all_clients():
    return db_entity.request("SELECT * FROM b_b.t_clients;")


def get_client_info(client_id: str):
    return db_entity.request("SELECT * FROM b_b.t_clients WHERE id = %s;" % (client_id), return_all=False)


def delete_client_by_id(client_id: str):
    if not client_already_exist_by_id(client_id):
        return [False, f"Клиент с id {client_id} не был найден!"]
    del_res = db_entity.insert_delete("DELETE FROM b_b.t_clients WHERE id = %s;" % (client_id))
    if not del_res[0]:
        return del_res
    else:
        return [True, f"Клиент с id {client_id} успешно удален!"]


def create_new_client(client_name: str):
    if len(client_name) == 0 or len(client_name) > 50:
        return [False, "Было передано недопустимое наименование клиента. Наименование клиента не должно превышать 50 символов!"]
    elif client_already_exist_by_name(client_name):
        return [False, f"Клиент с таким наименованием '{client_name}' уже существует!"]

    create_res = db_entity.insert_delete("INSERT INTO b_b.t_clients (name) VALUES ('%s');" % (client_name))
    if not create_res[0]:
        return create_res
    else:
        return [True, f"Клиент с наименованием '{client_name}' успешно создан!"]


def change_client_activity(client_id: str):
    client_info = get_client_info(client_id)
    if not len(client_info):
        return [False, f"Клиент с таким id '{client_id}' не был найден!"]

    create_res = db_entity.insert_delete("UPDATE b_b.t_clients SET active = %s WHERE id = %s;" % (not client_info[2], client_id))
    if not create_res[0]:
        return create_res
    else:
        if not client_info[2] is True:
            act = 'активирован'
        else:
            act = 'дективирован'
        return [True, f"Клиент '{client_info[1]}' успешно {act}!"]


def change_client_key(client_id: str):
    client_info = get_client_info(client_id)
    if not len(client_info):
        return [False, f"Клиент с таким id '{client_id}' не был найден!"]
    new_key = Fernet.generate_key().decode()

    create_res = db_entity.insert_delete("UPDATE b_b.t_clients SET key = '%s' WHERE id = %s;" % (new_key, client_id))
    if not create_res[0]:
        return create_res
    else:
        return [True, f"Клиент '{client_info[1]}' успешно присвоен кллюч :\n{new_key}!"]


# USERS

def user_telegram_access(user_id: str):
    res = db_entity.request("SELECT telegram_access FROM b_b.t_telegram_users WHERE user_id = '%s';" % (user_id), return_all=False)
    if len(res) == 0 or res[0] is False:
        return False
    else:
        return True


def get_user_info(user_id: str):
    return db_entity.request("SELECT * FROM b_b.t_telegram_users WHERE user_id = '%s';" % (user_id), return_all=False)


def user_already_exist(user_id: str):
    res = db_entity.request("SELECT user_id FROM b_b.t_telegram_users WHERE user_id = '%s';" % (user_id))
    if len(res) == 0:
        return False
    else:
        return True


def get_all_users():
    return db_entity.request("SELECT * FROM b_b.t_telegram_users;")


def delete_user_by_id(user_id: str):
    if not user_already_exist(user_id):
        return [False, f"Пользователь с id {user_id} не был найден!"]
    del_res = db_entity.insert_delete("DELETE FROM b_b.t_telegram_users WHERE user_id = '%s';" % (user_id))
    if not del_res[0]:
        return del_res
    else:
        return [True, f"Пользователь с id {user_id} успешно удален!"]


def create_new_user(user_id: str, user_name: str):
    if len(user_id) == 0 or len(user_id) != 9:
        return [False, "Был передан недопустимый ID пользователя!"]
    elif len(user_name) == 0 or len(user_name) > 50:
        return [False, "Было передано недопустимое имя пользователя. Имя пользователя не должно превышать 50 символов!"]
    elif user_already_exist(user_id):
        return [False, f"Пользователь с таким id {user_id} уже существует!"]

    res = db_entity.insert_delete("INSERT INTO b_b.t_telegram_users (user_id, name) VALUES ('%s', '%s');" % (user_id, user_name))
    if not res[0]:
        return res
    else:
        return [True, f"Пользователь {user_name} с id {user_id} успешно создан!"]


def change_user_telegram_access(user_id: str):
    user_info = get_user_info(user_id)
    if not len(user_info):
        return [False, f"Пользователь с таким id '{user_id}' не был найден!"]

    res = db_entity.insert_delete("UPDATE b_b.t_telegram_users SET telegram_access = %s WHERE user_id = '%s';" % (not user_info[3], user_id))
    if not res[0]:
        return res
    else:
        return [True, f"Доуступ пользователя '{user_info[1]}' в телеграм изменен на {not user_info[3]}!"]


def change_user_key(user_id: str):
    user_info = get_user_info(user_id)
    if not len(user_info):
        return [False, f"Пользователь с таким id '{user_id}' не был найден!"]
    new_key = Fernet.generate_key().decode()

    res = db_entity.insert_delete("UPDATE b_b.t_telegram_users SET key = '%s' WHERE user_id = '%s';" % (new_key, user_id))
    if not res[0]:
        return res
    else:
        return [True, f"Пользователю '{user_info[1]}' успешно присвоен кллюч :\n{new_key}!"]