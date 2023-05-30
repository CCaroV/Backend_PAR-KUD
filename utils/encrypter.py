from os import getenv

from cryptography.fernet import Fernet


def encryptData(data: dict):
    encriptador = Fernet(getenv("SECRET"))
    data['user'] = encriptador.encrypt(data['user'].encode())
    data['password'] = encriptador.encrypt(data['password'].encode())
    return data


def decryptData(data: dict):
    encriptador = Fernet(getenv("SECRET"))
    data['user'] = encriptador.decrypt(data['user'].encode())
    data['password'] = encriptador.decrypt(data['password'].encode())
    return data
