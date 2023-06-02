from flask import Blueprint, request, jsonify

from utils.function_general import requestDB, requestDBnoReturn
from utils.function_jwt import validate_token
from utils.functions_db import conectarBD, conectarBDAuth

routes_user_auth = Blueprint("routes_user_auth", __name__)


@routes_user_auth.before_request
def verify_token_middleware():
    if request.get_json()['admin']:
        token = request.headers['Authorization'].split(" ")[1]
        response = validate_token(token)


@routes_user_auth.route("/cliente/registro", methods=['POST'])
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
        return jsonify({'error': str(e)}), 500


@routes_user_auth.route("/cliente/registro/clave", methods=['POST'])
def add_cliente_pass():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
        # Parametros del procedimiento o funcion
        par = (info_result["nombre_usuario_p"],
               info_result["clave_nueva_p"])
        requestDBnoReturn(DBconn, 'PARQUEADERO.PRIMER_CAMBIO_CLAVE_PR', par)
        # Recuperar los resultados, si los hay
        return 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
