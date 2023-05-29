from flask import Blueprint, request, jsonify

from functions_db import conectarBD, cerrarBD

routes_user_auth = Blueprint("routes_user_auth", __name__)


@routes_user_auth.route("/cliente", methods=['POST'])
def add_cliente():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD(request)

        # Crear un cursor
        cursor = DBconn.cursor()
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
