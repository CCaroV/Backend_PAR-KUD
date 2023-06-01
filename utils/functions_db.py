import base64
from os import getenv

import psycopg2
from flask import Flask, json, Request

from utils.encrypter import decrypt_dict
from utils.function_jwt import get_data

app = Flask(__name__)


def loadFileConfig():
    with open('./config.json') as f:
        data = json.load(f)
    return data


def conectarBD(request: Request):
    token = request.headers['Authorization'].split(" ")[1]
    key = base64.urlsafe_b64encode(str(getenv("SECRET")).encode('utf-8'))
    data = decrypt_dict(get_data(token),key)
    dataConn = loadFileConfig()
    conn = psycopg2.connect(host=dataConn["host"], port=dataConn["port"], database=dataConn["database"],
                            user=data["user"], password=data["password"])
    return conn


def cerrarBD(DBconection):
    DBconection.close()


def guardarCambiosEnBD(curs):
    curs.execute("COMMIT")
