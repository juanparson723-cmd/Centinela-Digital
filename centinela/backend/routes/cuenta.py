
from flask import Blueprint, jsonify, request, session, current_app
from database import get_connection

cuenta_bp = Blueprint("cuenta", __name__)


def obtener_usuario_id():
    return session.get("usuario_id")


# 1. GET: Consultar los datos de la cuenta.
@cuenta_bp.get("/mi-cuenta")
def mi_cuenta():
    usuario_id = obtener_usuario_id()

    if not usuario_id:
        return jsonify({"error": "Debes iniciar sesión."}), 401

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                u.id_usuario,
                u.nombre,
                u.correo,
                u.fecha_creacion,
                r.nombre AS rol
            FROM usuarios AS u
            INNER JOIN roles AS r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s AND u.activo = 1
            LIMIT 1
            """,
            (usuario_id,)
        )

        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "No se encontró la cuenta."}), 404

        if usuario["fecha_creacion"]:
            usuario["fecha_creacion"] = usuario["fecha_creacion"].isoformat()

        return jsonify({
            "status": "ok",
            "usuario": usuario
        }), 200

    except Exception:
        current_app.logger.exception("Error al consultar la cuenta.")
        return jsonify({"error": "No fue posible consultar la cuenta."}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 2. GET: Consultar todos los reportes del usuario.
@cuenta_bp.get("/mis-reportes")
def mis_reportes():
    usuario_id = obtener_usuario_id()

    if not usuario_id:
        return jsonify({"error": "Debes iniciar sesión."}), 401

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                rp.folio,
                rp.titulo,
                rp.descripcion,
                rp.es_anonimo,
                rp.fecha_reporte,
                rp.fecha_actualizacion,
                cat.nombre AS categoria,
                est.nombre AS estado
            FROM reportes AS rp
            INNER JOIN categorias_violencia AS cat
                ON rp.id_categoria = cat.id_categoria
            INNER JOIN estados_reporte AS est
                ON rp.id_estado = est.id_estado
            WHERE rp.id_usuario = %s
              AND rp.fecha_eliminacion IS NULL
            ORDER BY rp.fecha_reporte DESC
            """,
            (usuario_id,)
        )

        reportes = cursor.fetchall()

        for reporte in reportes:
            if reporte["fecha_reporte"]:
                reporte["fecha_reporte"] = reporte["fecha_reporte"].isoformat()

            if reporte["fecha_actualizacion"]:
                reporte["fecha_actualizacion"] = (
                    reporte["fecha_actualizacion"].isoformat()
                )

        return jsonify({
            "status": "ok",
            "total": len(reportes),
            "reportes": reportes
        }), 200

    except Exception:
        current_app.logger.exception("Error al consultar los reportes.")
        return jsonify({"error": "No fue posible consultar los reportes."}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 3. GET: Consultar un reporte específico.
@cuenta_bp.get("/mis-reportes/<string:folio>")
def consultar_reporte(folio):
    usuario_id = obtener_usuario_id()

    if not usuario_id:
        return jsonify({"error": "Debes iniciar sesión."}), 401

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                rp.folio,
                rp.titulo,
                rp.descripcion,
                rp.es_anonimo,
                rp.fecha_reporte,
                rp.fecha_actualizacion,
                cat.nombre AS categoria,
                est.nombre AS estado
            FROM reportes AS rp
            INNER JOIN categorias_violencia AS cat
                ON rp.id_categoria = cat.id_categoria
            INNER JOIN estados_reporte AS est
                ON rp.id_estado = est.id_estado
            WHERE rp.folio = %s
              AND rp.id_usuario = %s
              AND rp.fecha_eliminacion IS NULL
            LIMIT 1
            """,
            (folio, usuario_id)
        )

        reporte = cursor.fetchone()

        if not reporte:
            return jsonify({"error": "Reporte no encontrado."}), 404

        for campo in ("fecha_reporte", "fecha_actualizacion"):
            if reporte[campo]:
                reporte[campo] = reporte[campo].isoformat()

        return jsonify({
            "status": "ok",
            "reporte": reporte
        }), 200

    except Exception:
        current_app.logger.exception("Error al consultar un reporte.")
        return jsonify({"error": "No fue posible consultar el reporte."}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 4. PUT: Modificar el título y la descripción de un reporte.
@cuenta_bp.put("/mis-reportes/<string:folio>")
def modificar_reporte(folio):
    usuario_id = obtener_usuario_id()

    if not usuario_id:
        return jsonify({"error": "Debes iniciar sesión."}), 401

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Debes enviar los datos en formato JSON."}), 400

    titulo = datos.get("titulo")
    descripcion = datos.get("descripcion")

    if not isinstance(titulo, str) or not isinstance(descripcion, str):
        return jsonify({"error": "El título y la descripción son obligatorios."}), 400

    titulo = titulo.strip()
    descripcion = descripcion.strip()

    if not titulo or not descripcion:
        return jsonify({"error": "No puedes dejar campos vacíos."}), 400

    if len(titulo) > 150:
        return jsonify({"error": "El título no puede superar 150 caracteres."}), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id_reporte
            FROM reportes
            WHERE folio = %s
              AND id_usuario = %s
              AND fecha_eliminacion IS NULL
            LIMIT 1
            """,
            (folio, usuario_id)
        )

        reporte = cursor.fetchone()

        if not reporte:
            return jsonify({"error": "Reporte no encontrado."}), 404

        cursor.execute(
            """
            UPDATE reportes
            SET titulo = %s,
                descripcion = %s
            WHERE id_reporte = %s
            """,
            (titulo, descripcion, reporte["id_reporte"])
        )

        connection.commit()

        return jsonify({
            "status": "ok",
            "message": "Reporte modificado correctamente."
        }), 200

    except Exception:
        if connection:
            connection.rollback()

        current_app.logger.exception("Error al modificar un reporte.")
        return jsonify({"error": "No fue posible modificar el reporte."}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 5. DELETE: Eliminación lógica de un reporte.
@cuenta_bp.delete("/mis-reportes/<string:folio>")
def eliminar_reporte(folio):
    usuario_id = obtener_usuario_id()

    if not usuario_id:
        return jsonify({"error": "Debes iniciar sesión."}), 401

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE reportes
            SET fecha_eliminacion = CURRENT_TIMESTAMP
            WHERE folio = %s
              AND id_usuario = %s
              AND fecha_eliminacion IS NULL
            """,
            (folio, usuario_id)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Reporte no encontrado."}), 404

        connection.commit()

        return jsonify({
            "status": "ok",
            "message": "Reporte eliminado correctamente."
        }), 200

    except Exception:
        if connection:
            connection.rollback()

        current_app.logger.exception("Error al eliminar un reporte.")
        return jsonify({"error": "No fue posible eliminar el reporte."}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
