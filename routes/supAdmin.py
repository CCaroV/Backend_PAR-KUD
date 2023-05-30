from flask import Blueprint, request, jsonify

from utils.function_general import requestDB
from utils.function_jwt import validate_token
from utils.functions_db import conectarBD

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
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
        # Parametros del procedimiento o funcion
        par = (
            info_result["tipo_identificacion_p"], info_result["numero_identificacion_p"],
            info_result["NOMBRE1_EMPLEADO_P"],
            info_result["NOMBRE2_EMPLEADO_P"], info_result["APELLIDO1_EMPLEADO_P"], info_result["APELLIDO2_CLIENTE_P"],
            info_result["TELEFONO_EMPLEADO_P"], info_result["CORREO_EMPLEADO_P"])
        return requestDB(DBconn, 'PARQUEADERO.CREAR_ADMIN_FU', par)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_SUser.route("/supAdmin/operador", methods=['POST'])
def set_operador():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        par = (
            info_result["tipo_identificacion_p"], info_result["numero_identificacion_p"],
            info_result["NOMBRE1_EMPLEADO_P"],
            info_result["NOMBRE2_EMPLEADO_P"], info_result["APELLIDO1_EMPLEADO_P"], info_result["APELLIDO2_CLIENTE_P"],
            info_result["TELEFONO_EMPLEADO_P"], info_result["CORREO_EMPLEADO_P"])

        return requestDB(DBconn, 'PARQUEADERO.CREAR_OPERADOR_FU', par)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
