from flask import Blueprint

from flask import Blueprint, request, jsonify

from utils.Exceptions import verifyExceptions
from utils.function_general import requestDB, requestDBnoReturn
from utils.function_jwt import validate_token
from utils.functions_db import *

routes_audit = Blueprint("routes_audit", __name__)


# verificar si el jwt esta activo
@routes_audit.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    response = validate_token(token)


@routes_audit.route("/auditoria", methods=['GET'])
def show_audit (cliente_id):
    def set_card():
        try:
            DBconn = conectarBD(request)
            return requestDB(DBconn, 'AUDITORIA.MOSTRAR_AUDITORIA_FU')

        except Exception as e:
            return verifyExceptions(e)
