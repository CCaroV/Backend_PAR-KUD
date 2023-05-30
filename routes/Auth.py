from flask import Blueprint, request, jsonify

from utils.function_general import requestDB
from utils.functions_db import conectarBD

routes_user_auth = Blueprint("routes_user_auth", __name__)


@routes_user_auth.route("/cliente", methods=['POST'])
def add_cliente():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
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
