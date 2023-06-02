from flask import Blueprint, request, jsonify

from utils.function_general import requestDB, requestDBnoReturn, requestDBLog
from utils.function_jwt import validate_token
from utils.functions_db import conectarBD, conectarBDAuth, conectarBDLog
from functools import wraps

routes_user_auth = Blueprint("routes_user_auth", __name__)


def verify_token_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.get_json().get('admin'):
            token = request.headers.get('Authorization', '').split(" ")[1]
            response = validate_token(token)
            # Aquí puedes realizar acciones adicionales con la respuesta si es necesario
            # ...
        return func(*args, **kwargs)

    return wrapper


@routes_user_auth.route("/cliente/registro", methods=['POST'])
@verify_token_middleware
def add_cliente():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = None
        if info_result['admin']:
            DBconn = conectarBD(request)
        else:
            DBconn = conectarBDAuth(request)

        # Parametros del procedimiento o funcion
        par = (info_result["tipo_identificacion_p"],
               info_result["numero_identificacion_p"],
               info_result["nombre1_cliente_p"],
               info_result["nombre2_cliente_p"],
               info_result["apellido1_cliente_p"],
               info_result["apellido2_cliente_p"],
               info_result["telefono_cliente_p"],
               info_result["correo_cliente_p"]
               )
        # Recuperar los resultados, si los hay
        return requestDB(DBconn, 'PARQUEADERO.CREAR_CLIENTE_FU', par)

    except Exception as e:
        if "password authentication failed for user" in str(e):
            return {'error': "Password does not match"}, 401
        if "already exists" in str(e):
            return {'error': 'El usuario ya existe'}, 409
        if 'Este correo ya está registrado en la base de datos' in str(e):
            return {'error': 'email already registered'}, 409
        return jsonify({'error': str(e)}), 500


@routes_user_auth.route("/cliente/registro/clave", methods=['POST'])
@verify_token_middleware
def add_cliente_pass():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBDAuth(request)
        # Parametros del procedimiento o funcion
        par = (info_result["nombre_usuario_p"],
               info_result["clave_nueva_p"])
        requestDBnoReturn(DBconn, 'PARQUEADERO.PRIMER_CAMBIO_CLAVE_PR', par)
        # Recuperar los resultados, si los hay
        return jsonify({'success': 'password changed'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_user_auth.route("/cliente/login", methods=['POST'])
def cliente_login():
    try:
        info_result = request.get_json()
        DBconn = conectarBDLog(info_result)
        return requestDB(DBconn, 'PARQUEADERO.MOSTRAR_ROL_USUARIO_FU')

    except Exception as e:
        if 'password authentication failed for user' in str(e):
            return {'error': "Password does not match"}, 401
        return jsonify({'error': str(e)}), 500
