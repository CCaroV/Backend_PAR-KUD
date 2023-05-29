from flask import jsonify
from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime, timedelta


def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date


def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2)},key=getenv("SECRET"), algorithm="HS256")
    return token.encode("UTF-8")


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


