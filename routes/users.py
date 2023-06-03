from flask import Blueprint, request, jsonify

from utils.Exceptions import verifyExceptions
from utils.function_general import requestDB, requestDBnoReturn
from utils.function_jwt import validate_token
from utils.functions_db import *

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
        cursor.execute("SELECT * FROM PARQUEADERO.CLIENTE WHERE K_CLIENTE = " + str(cliente_id))

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results), 200

    except Exception as e:
        return verifyExceptions(e)


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
        return jsonify(results), 200

    except Exception as e:
        return verifyExceptions(e)


# Función para mostrar los vehículos que un cliente tiene registrados.
@routes_user.route("/cliente/vehiculos", methods=['POST'])
def get_vehiculos():
    try:
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_VEHICULOS_CLIENTE_FU')

    except Exception as e:
        return verifyExceptions(e)


@routes_user.route("/cliente/registro/vehiculo", methods=['POST'])
def set_vehicle():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Parametros del procedimiento o funcion
        par = (
            info_result["tipo_vehiculo_p"],
            info_result["placa_p"],
            info_result["nombre_1_p"],
            info_result["nombre_2_p"],
            info_result["apellido_1_p"],
            info_result["apellido_2_p"],
            info_result["marca_vehiculo_p"],
            info_result["color_vehiculo_p"]
        )
        requestDBnoReturn(DBconn, 'PARQUEADERO.AGREGAR_VEHICULO_PR', par)
        return {'success': "vehicle registered"}, 200

    except Exception as e:
        return verifyExceptions(e)


@routes_user.route("/cliente/registro/tarjeta", methods=['POST'])
def set_card():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Parametros del procedimiento o funcion
        par = (
            info_result["nombre_duenio_tarjeta_p"],
            info_result["apellido_duenio_tarjeta_p"],
            info_result["numero_tarjeta_p"],
            info_result["ultimos_cuatro_digitos_p"],
            info_result["mes_vencimiento_p"],
            info_result["anio_vencimiento_p"],
            info_result["tipo_tarjeta_p"]
        )
        requestDBnoReturn(DBconn, 'PARQUEADERO.INSERTAR_METODO_PAGO_PR', par)
        return {'success': "card registered"}, 200

    except Exception as e:
        return verifyExceptions(e)


@routes_user.route("/cliente/reservas", methods=['POST'])
def get_reserve():
    try:
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_RESERVAS_CLIENTE_FU')

    except Exception as e:
        return jsonify({'error': str(e)}), 500