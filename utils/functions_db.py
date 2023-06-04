import base64
from os import getenv

import psycopg2
from flask import Flask, json, Request

from utils.encrypter import decrypt_dict
from utils.function_jwt import get_data

app = Flask(__name__)


# patron singleton para los datos de la base de datos desde el json
class ConfigLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = None
        return cls._instance

    def loadFileConfig(self):
        if self._config is None:
            with open('./config.json') as f:
                self._config = json.load(f)
        return self._config


def conectarBD(request: Request):
    token = request.headers['Authorization'].split(" ")[1]
    key = "NwKyZF848xFHInNmjQfY4U4uKTNGhK2ABqgHvolGhuA="
    data = decrypt_dict(get_data(token), key)
    config_loader = ConfigLoader()
    dataConn = config_loader.loadFileConfig()
    conn = psycopg2.connect(host=dataConn["host"], port=dataConn["port"], database=dataConn["database"],
                            user=data["user"], password=data["password"])
    return conn


def conectarBDAuth(request: Request):
    key = "NwKyZF848xFHInNmjQfY4U4uKTNGhK2ABqgHvolGhuA="
    config_loader = ConfigLoader()
    dataConn = config_loader.loadFileConfig()
    conn = psycopg2.connect(host=dataConn["host"], port=dataConn["port"], database=dataConn["database"],
                            user="manage_account_user", password="CA1234")
    return conn


def conectarBDLog(request: Request):
    config_loader = ConfigLoader()
    dataConn = config_loader.loadFileConfig()
    conn = psycopg2.connect(host=dataConn["host"], port=dataConn["port"], database=dataConn["database"],
                            user=request['user'], password=request["password"])
    return conn


def cerrarBD(DBconection):
    DBconection.close()


def guardarCambiosEnBD(curs):
    curs.execute("COMMIT")
