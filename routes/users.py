from flask import Blueprint, request, jsonify

from function_jwt import write_token, validate_token, get_data
from functions_db import *

routes_user = Blueprint("routes_user", __name__)
routes_user_auth = Blueprint("routes_user_auth", __name__)
routes_SUser = Blueprint("routes_SUser", __name__)


# verificar si el jwt esta activo
@routes_user.before_request
@routes_SUser.before_request
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


@routes_user_auth.route("/cliente", methods=['POST'])
def add_cliente():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # info_result = request.get_json()
        # todo eliminar este diccionario y habilitar el info_result
        info_result = {
            "tipo_id": "CC",
            "num_id": "1013680174",
            "f_nom": "Juan",
            "s_nom": "Camilo",
            "f_apell": "Cespedes",
            "s_apell": "Romero",
            "tel": "3123566333",
            "email": "juankamilocromero@gmail.com"
        }
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()
        # Parametros del procedimiento o funcion
        par = (info_result["tipo_id"], info_result["num_id"], info_result["f_nom"], info_result["s_nom"],
               info_result["f_apell"], info_result["s_apell"], info_result["tel"], info_result["email"])
        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CREAR_CLIENTE_FU', par)

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


@routes_user.route("/verificarDispo", methods=['GET'])
def get_disponibilidad():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()
        # Parametros del procedimiento o funcion
        par = (info_result["nombre_ciudad_p"], info_result["tipo_vehiculo_p"], info_result["es_cubierto_p"],
               info_result["fecha_entrada_p"], info_result["hora_entrada_p"], info_result["s_apell"],
               info_result["tel"], info_result["nombre_entrada_p"], info_result["nombre_sucursal_p"])

        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.VERIFICAR_DISPONIBILIDAD_FU', par)

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


@routes_user.route("/cliente/vehiculo", methods=['POST'])
def set_vehiculo():
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
            info_result["tipo_vehiculo_p"], info_result["placa_p"], info_result["nombre_1_p"],
            info_result["nombre_2_p"],
            info_result["apellido_1_p"], info_result["apellido_2_p"], info_result["marca_vehiculo_p"],
            info_result["color_vehiculo_p"])

        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.VERIFICAR_DISPONIBILIDAD_FU', par)

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

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
