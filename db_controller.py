import db_entity


def get_code(name_id: str):
    return db_entity.request(f"SELECT code FROM t_code WHERE name_id = {name_id}", False)


def get_client_subscription(subscription_serial_key: str):
    return db_entity.request(f"SELECT * FROM t_clients_subscription "
                             f"INNER JOIN t_clients ON t_clients_subscription.client_id = t_clients.id"
                             f"WHERE t_clients_subscription.serial_key = {subscription_serial_key}"
                             f"ORDER BY t_clients_subscription.validity_date DESC", False)
