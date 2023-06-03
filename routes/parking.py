import logging

from flask import Blueprint, request, jsonify

from utils.Exceptions import verifyExceptions
from utils.function_general import requestDB
from utils.function_jwt import validate_token
from utils.functions_db import *

routes_parking = Blueprint("routes_parking", __name__)


@routes_parking.before_request
def verify_token_middleware():
    token = request.headers['AUTHORIZATION'].split(" ")[1]
    validate_token(token)


@routes_parking.route("/cliente/parqueaderos", methods=['GET'])
def get_parqueaderos():
    try:
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_SUCURSALES_FU')

    except Exception as e:
        return verifyExceptions(e)


@routes_parking.route("/cliente/vehiculos/marcas", methods=["GET"])
def get_marcas():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()

        # Ejecutar el procedimiento almacenado
        # cursor.callproc('nombre_procedimiento', parametros)
        cursor.execute("SELECT * FROM PARQUEADERO.MARCA_VEHICULO")

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results), 200

    except Exception as e:
        return verifyExceptions(e)

