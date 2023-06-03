from flask import Blueprint, request, jsonify

from utils.function_general import requestDB, requestDBnoReturn
from utils.function_jwt import validate_token
from utils.functions_db import conectarBD

routes_admin_subsidiaries = Blueprint("routes_admin_subsidiaries", __name__)


@routes_admin_subsidiaries.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = validate_token(token)


@routes_admin_subsidiaries.route("/admin/sucursal/tarifa", methods=['POST'])
def change_subsidiary_fee():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)
        # Parametros del procedimiento o funcion
        par = (
            info_result["nombre_sucursal_p"],
            info_result["ciudad_p"],
            info_result["tipo_sucursal_p"],
            info_result["direccion_sucursal_p"],
            info_result["tipo_tarifa_p"],
            info_result["valor_tarifa_p"]
        )

        requestDBnoReturn(DBconn, 'PARQUEADERO.MODIFICAR_TARIFA_SUCURSAL_PR', par)
        return {'success': "fee changed"}, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_admin_subsidiaries.route("/admin/sucursal/horario", methods=['POST'])
def change_subsidiary_schedule():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        par = (
            info_result["nombre_sucursal_p"],
            info_result["ciudad_p"],
            info_result["tipo_sucursal_p"],
            info_result["direccion_sucursal_p"],
            info_result["dia_semana_p"],
            info_result["hora_abierto_p"],
            info_result["hora_cerrado_p"],
            info_result["es_horario_completo_p"],
            info_result["es_cerrado_completo_p"]
        )
        requestDB(DBconn, 'MODIFICAR_HORARIO_SUCURSAL_PR', par)
        return {'success': "fee changed"}, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
