from flask import Blueprint, request, jsonify

from function_jwt import validate_token
from functions_db import conectarBD, cerrarBD

routes_SUser = Blueprint("routes_SUser", __name__)


@routes_SUser.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = validate_token(token)


@routes_SUser.route("/supAdmin/admin", methods=['POST'])
def set_admin():
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
            info_result["tipo_identificacion_p"], info_result["numero_identificacion_p"],
            info_result["NOMBRE1_EMPLEADO_P"],
            info_result["NOMBRE2_EMPLEADO_P"], info_result["APELLIDO1_EMPLEADO_P"], info_result["APELLIDO2_CLIENTE_P"],
            info_result["TELEFONO_EMPLEADO_P"], info_result["CORREO_EMPLEADO_P"])

        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CREAR_ADMIN_FU', par)

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


@routes_SUser.route("/supAdmin/operador", methods=['POST'])
def set_operador():
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
            info_result["tipo_identificacion_p"], info_result["numero_identificacion_p"],
            info_result["NOMBRE1_EMPLEADO_P"],
            info_result["NOMBRE2_EMPLEADO_P"], info_result["APELLIDO1_EMPLEADO_P"], info_result["APELLIDO2_CLIENTE_P"],
            info_result["TELEFONO_EMPLEADO_P"], info_result["CORREO_EMPLEADO_P"])

        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CREAR_OPERADOR_FU', par)

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
