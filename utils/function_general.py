from flask import jsonify
from psycopg2._psycopg import connection

from utils.functions_db import cerrarBD


def requestDB(dbConn: connection, plPsql: str, par: tuple = ()):
    cursor = dbConn.cursor()
    cursor.callproc(plPsql, par)
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
    cerrarBD(dbConn)
    return jsonify(results[0][2])
