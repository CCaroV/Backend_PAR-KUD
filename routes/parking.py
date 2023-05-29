from flask import Blueprint, request, jsonify

from function_jwt import validate_token
from functions_db import *

routes_parking = Blueprint("routes_parking", __name__)


@routes_parking.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = validate_token(token)


@routes_parking.route("/cliente/parqueaderos", methods=['GET'])
def get_parqueaderos():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.MOSTRAR_SUCURSALES_FU', ())
        # print("SELECT * FROM PARQUEADERO.SUCURSAL")
        # cursor.execute("SELECT * FROM PARQUEADERO.SUCURSAL")
        print(cursor)
        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        if results:
            # Crear una lista para almacenar los diccionarios de los resultados
            data = []

            # Iterar sobre los resultados y construir los diccionarios
            for result in results:
                # Obtener los elementos internos de cada resultado
                inner_results = result[0]

                # Extender la lista de diccionarios con los elementos internos
                data.extend(inner_results)

            # Devolver la lista de diccionarios como respuesta en formato JSON
            return jsonify(data)

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results[0][2])

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
        print("SELECT * FROM PARQUEADERO.MARCA_VEHICULO")
        cursor.execute("SELECT * FROM PARQUEADERO.MARCA_VEHICULO")

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Función que retorna información básica de sucursales dado unos parámetros de entrada.
@routes_parking.route("/cliente/sucursales", methods=['POST'])
def get_sucursal():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()
        # Parametros del procedimiento o funcion
        par = (
            info_result["tipo_vehiculo_p"],
            info_result["ciudad_p"],
            info_result["es_parq_encubierto_p"],
            info_result["nombre_sucursal_p"]
        )

        # Ejecutar el procedimiento almacenado
        cursor.callproc('MOSTRAR_INFO_BASICA_SUCURSAL_FU', par)

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()
        if results:
            # Crear una lista para almacenar los diccionarios de los resultados
            data = []

            # Iterar sobre los resultados y construir los diccionarios
            for result in results:
                # Obtener los elementos internos de cada resultado
                inner_results = result[0]

                # Extender la lista de diccionarios con los elementos internos
                data.extend(inner_results)

            # Devolver la lista de diccionarios como respuesta en formato JSON
            return jsonify(data)

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results[0][2])

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Función que muestra la información de la sucursal en el último paso de reserva en la aplicación
@routes_parking.route("/cliente/sucursal/reserva", methods=['POST'])
def get_sucursal_final():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()
        # Parametros del procedimiento o funcion
        par = (
            info_result["ciudad_p"],
            info_result["es_parq_cubierto_p"],
            info_result["tipo_parqueadero_p"],
            info_result["nombre_sucursal_p"]
        )

        # Ejecutar el procedimiento almacenado
        cursor.callproc('MOSTRAR_INFO_SUCURSAL_RESERVA_FU', par)

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()
        if results:
            # Crear una lista para almacenar los diccionarios de los resultados
            data = []

            # Iterar sobre los resultados y construir los diccionarios
            for result in results:
                # Obtener los elementos internos de cada resultado
                inner_results = result[0]

                # Extender la lista de diccionarios con los elementos internos
                data.extend(inner_results)

            # Devolver la lista de diccionarios como respuesta en formato JSON
            return jsonify(data)

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results[0][2])

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Función que retorna la información de los métodos de pago de un cliente para pagar una reserva.
@routes_parking.route("/cliente/metodosDePago", methods=['GET'])
def get_metodos_pagos():
    try:
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.callproc('MOSTRAR_METODOS_PAGO_FU', ())

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()
        if results:
            # Crear una lista para almacenar los diccionarios de los resultados
            data = []

            # Iterar sobre los resultados y construir los diccionarios
            for result in results:
                # Obtener los elementos internos de cada resultado
                inner_results = result[0]

                # Extender la lista de diccionarios con los elementos internos
                data.extend(inner_results)

            # Devolver la lista de diccionarios como respuesta en formato JSON
            return jsonify(data)

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results[0][2])

    except Exception as e:
        return jsonify({'error': str(e)}), 500