from flask import Blueprint, request, jsonify

from utils.function_general import requestDB, requestDBnoReturn
from utils.function_jwt import validate_token
from utils.functions_db import *

routes_reserve = Blueprint("routes_reserve", __name__)


# verificar si el jwt esta activo
@routes_reserve.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = validate_token(token)


# El cliente selecciona el tipo de vehículo. La función retorna los vehículos del cliente registrados de ese tipo.
@routes_reserve.route("/cliente/vehiculos/tipo", methods=['POST'])
def get_vehiculos_tipo():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Parametros del procedimiento o funcion
        par = (
            info_result["tipo_vehiculo_p"]
        )

        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_VEHICULOS_RESERVA_FU', par)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 2. El cliente escoge la ciudad y sucursal en la que desea reservar. También escoge si el parqueadero debe o no ser
# cubierto. La función retorna la ciudad y sucursal que se corresponda con esos valores, verificando que haya
# disponibilidad.
@routes_reserve.route("/cliente/sucursales", methods=['POST'])
def get_sucursal():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        par = (
            info_result["tipo_vehiculo_p"],
            info_result["ciudad_p"],
            info_result["es_parq_encubierto_p"],
            info_result["nombre_sucursal_p"]
        )

        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_INFO_BASICA_SUCURSAL_FU', par)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -- 3. El usuario selecciona la sucursal en la que desea reservar, la función recibe estos parámetros.
# -- La función vuelve a verificar que la sucursal escogida tenga cupos disponibles.
# -- La función devuelve mayor información de la sucursal como su dirección y tarifa con recargos incluidos,
# -- esto con el fin de que el cliente esté seguro de escoger la sucursal correcta para su reserva.
@routes_reserve.route("/cliente/sucursal/reserva", methods=['POST'])
def get_sucursal_final():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        DBconn = conectarBD(request)

        # Parametros del procedimiento o funcion
        par = (
            info_result["ciudad_p"],
            info_result["es_parq_cubierto_p"],
            info_result["tipo_parqueadero_p"],
            info_result["nombre_sucursal_p"]
        )

        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_INFO_SUCURSAL_RESERVA_FU', par)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 4. Una vez seleccionada la sucursal, el cliente debe seleccionar un método de pago.
# La función devuelve la información básica de sus métodos de pago registrados.
@routes_reserve.route("/cliente/metodosDePago", methods=['POST'])
def get_metodos_pagos():
    try:
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_METODOS_PAGO_FU')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 5. Una vez seleccionada el vehículo, sucursal y método de pago, se hace la reserva en la BD.
@routes_reserve.route("/cliente/reservar", methods=['POST'])
def set_reserve ():
    try:
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
        par = (
            info_result["tipo_vehiculo_p"],
            info_result["marca_placa_vehiculo_p"],
            info_result["es_parq_cubierto_p"],
            info_result["ciudad_p"],
            info_result["nombre_sucursal_p"],
            info_result["direccion_sucursal_p"],
            info_result["fecha_reserva_p"],
            info_result["hora_reserva_p"],
            info_result["ultimos_cuatro_digitos_p"],
            info_result["tipo_tarjeta_p"],
            info_result["nombre_duenio_tarjeta_p"],
            info_result["apellido_duenio_tarjeta_p"],
            info_result["puntos_usados_p"]
        )
        requestDBnoReturn(DBconn, 'PARQUEADERO.CREAR_RESERVA_PR',par)
        return {'success': 'successful reservation'}, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
