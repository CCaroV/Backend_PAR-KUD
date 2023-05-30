from cryptography import fernet
from flask import jsonify
from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime, timedelta

from utils.encrypter import encryptData


def expire_date(hour: int):
    now = datetime.now()
    new_date = now + timedelta(hours=hour)
    return new_date


def write_token(data: dict):
    dataEncrypt = encryptData(data)
    token = encode(payload={**dataEncrypt, "exp": expire_date(1)}, key=getenv("SECRET"), algorithm="HS256")
    return verifyEncode(token)


def verifyEncode(string):
    try:
        encoded = string.encode('utf-8')
        return encoded
    except AttributeError:
        return string


def validate_token(token, output=False):
    try:
        if output:
            response = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
            return response
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response


def get_data(token):
    return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
