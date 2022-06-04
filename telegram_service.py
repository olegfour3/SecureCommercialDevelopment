import db_controller as db

# CLIENTS


def get_message_all_clients():  # не используется
    res = db.get_all_clients()
    if len(res) == 0:
        return 'Пока что нет ни одного клиента'
    ans_list = []
    i = 1
    for id, name, unt, active in res:
        ans_list.append(f'{i}) Наименование: {name} УНП: {unt} Активный: {active} ИД: {id}')
        i += 1
    ans = '\n'.join(ans_list)
    return ans


def get_all_clients():
    return db.get_all_clients()


def get_client_info(client_id: str):
    return db.get_client_info(client_id)


def delete_client(client_id: str):
    res = db.delete_client_by_id(client_id)
    return res[1]


def create_new_client(client_name: str):
    return db.create_new_client(client_name)


# USERS


def get_all_users():
    return db.get_all_users()


def get_message_all_users():  # не используется
    res = db.get_all_users()
    if len(res) == 0:
        return 'Пока что нет ни одного пользователя'
    ans_list = []
    i = 1
    for x, y in res:
        ans_list.append(f'{i}) ' + x + ' | ' + y)
        i += 1
    ans = '\n'.join(ans_list)
    return ans


def delete_user(user_id: str):
    res = db.delete_user_by_id(user_id)
    return res[1]


def user_already_exist(user_id: str):
    return db.user_already_exist(user_id)


def create_new_user(user_id: str, user_name: str):
    return db.create_new_user(user_id, user_name)
