import psycopg2
from flask import Flask, json, Request
from flask_cors import CORS

from utils.function_jwt import get_data
from utils.encrypter import decrypt_dict

app = Flask(__name__)
cors = CORS(app)


def loadFileConfig():
    with open('./config.json') as f:
        data = json.load(f)
    return data


def conectarBD(request: Request):
    token = request.headers['Authorization'].split(" ")[1]
    data = decrypt_dict(get_data(token))
    dataConn = loadFileConfig()
    conn = psycopg2.connect(host=dataConn["host"], port=dataConn["port"], database=dataConn["database"],
                            user=data["user"], password=data["password"])
    return conn


def cerrarBD(DBconection):
    DBconection.close()


def guardarCambiosEnBD(curs):
    curs.execute("COMMIT")
