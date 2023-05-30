from flask import Blueprint, request, jsonify

from function_jwt import write_token, validate_token, get_data
from functions_db import *

routes_user = Blueprint("routes_user", __name__)


# verificar si el jwt esta activo
@routes_user.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = validate_token(token)


@routes_user.route("/cliente/<string:cliente_id>", methods=['GET'])
def get_clienteByid(cliente_id):
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()

        # Ejecutar el procedimiento almacenado
        # cursor.callproc('', parametros)
        print("SELECT * FROM PARQUEADERO.CLIENTE")
        cursor.execute("SELECT * FROM PARQUEADERO.CLIENTE WHERE K_CLIENTE = " + str(cliente_id))

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_user.route("/cliente/<string:emailCliente>", methods=['POST'])
def post_newClaveCliente(emailCliente):
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # info_result = request.get_json()
        # todo eliminar este diccionario y habilitar el info_result
        info_result = {
            "clave_nueva": "3123566333",
        }
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()
        # Parametros del procedimiento o funcion
        par = (emailCliente, info_result["clave_nueva"])
        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CAMBIO_CLAVE_USUARIO_PR', par)
        # Commit en BD
        guardarCambiosEnBD()
        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Función para mostrar los vehículos que un cliente tiene registrados.
@routes_user.route("/cliente/vehiculos", methods=['POST'])
def get_vehiculos():
    try:
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()
        # Parametros del procedimiento o funcion

        # Ejecutar el procedimiento almacenado
        cursor.callproc('MOSTRAR_VEHICULOS_CLIENTE_FU', ())

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


# Función que devuelve los vehículos de un cliente según el tipo de vehículo.
@routes_user.route("/cliente/vehiculos/tipo", methods=['POST'])
def get_vehiculos_tipo():
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
            info_result["tipo_vehiculo_p"]
        )

        # Ejecutar el procedimiento almacenado
        cursor.callproc('MOSTRAR_VEHICULOS_RESERVA_FU', par)

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
