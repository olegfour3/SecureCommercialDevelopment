from cryptography.fernet import Fernet

#key = "qY9DQub0XejtqQm7uC8_gONuhDNqmgnNWdzQtwII5OA="


def encode(key, data):
    fernet = Fernet(key)
    enctex = fernet.encrypt(data.encode())
    return enctex.decode('utf8')


def decode(key, data):
    fernet = Fernet(key)
    dectex = fernet.decrypt(bytes(data, encoding='utf8'))
    return dectex.decode('utf8')

