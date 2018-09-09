import hashlib


def get_salt():
    with open('.secret_salt', 'rt') as salt:
        return salt.read()


def hash_string(string, salt):
    if string == '':
        return None
    salted_string = string + salt
    m = hashlib.sha256(salted_string.encode('utf-8'))
    return m.hexdigest()

