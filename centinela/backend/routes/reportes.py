import hashlib
import hmac
import secrets

from flask import Blueprint, jsonify, request, session, current_app

from database import get_connection

reportes_bp = Blueprint("reportes", __name__)


@reportes_bp.get("/categorias")
def obtener_categorias():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id_categoria, nombre, descripcion
            FROM categorias_violencia
            WHERE activa = TRUE
            ORDER BY nombre
            """
        )

        return jsonify({
            "categorias": cursor.fetchall()
        }), 200

    except Exception:
        current_app.logger.exception(
            "Error al consultar categorías"
        )

        return jsonify({
            "error": "No fue posible obtener las categorías"
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@reportes_bp.post("/reportes")
def crear_reporte():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Se esperaba un objeto JSON"
        }), 400

    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    id_categoria = data.get("id_categoria")
    es_anonimo = data.get("es_anonimo", True)
    ubicacion = data.get("ubicacion", {})

    if not isinstance(titulo, str) or not titulo.strip():
        return jsonify({
            "error": "El título es obligatorio"
        }), 400

    if not isinstance(descripcion, str) or not descripcion.strip():
        return jsonify({
            "error": "La descripción es obligatoria"
        }), 400

    titulo = titulo.strip()
    descripcion = descripcion.strip()

    if len(titulo) > 150:
        return jsonify({
            "error": "El título no puede superar los 150 caracteres"
        }), 400

    if len(descripcion) > 10000:
        return jsonify({
            "error": "La descripción es demasiado extensa"
        }), 400

    if (
        isinstance(id_categoria, bool)
        or not isinstance(id_categoria, int)
        or id_categoria <= 0
    ):
        return jsonify({
            "error": "Selecciona una categoría válida"
        }), 400

    if not isinstance(es_anonimo, bool):
        return jsonify({
            "error": "El campo es_anonimo debe ser verdadero o falso"
        }), 400

    if not isinstance(ubicacion, dict):
        return jsonify({
            "error": "La ubicación tiene un formato inválido"
        }), 400

    campos_ubicacion = (
        "estado", "municipio", "colonia", "referencia"
    )

    for campo in campos_ubicacion:
        valor = ubicacion.get(campo)

        if valor is not None and (
            not isinstance(valor, str) or len(valor) > 255
        ):
            return jsonify({
                "error": f"El campo de ubicación '{campo}' es inválido"
            }), 400

    # El código original solo se devuelve una vez.
    codigo_privado = secrets.token_urlsafe(24)
    codigo_hash = hashlib.sha256(
        codigo_privado.encode("utf-8")
    ).hexdigest()

    folio = "CD-" + secrets.token_hex(8).upper()

    usuario_id = None if es_anonimo else session.get("usuario_id")

    if not es_anonimo and not usuario_id:
        return jsonify({
            "error": "Debes iniciar sesión para registrar un reporte identificado"
        }), 401

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Confirmar que la categoría existe y está activa.
        cursor.execute(
            """
            SELECT id_categoria
            FROM categorias_violencia
            WHERE id_categoria = %s
              AND activa = TRUE
            """,
            (id_categoria,),
        )

        if not cursor.fetchone():
            return jsonify({
                "error": "La categoría seleccionada no existe o está inactiva"
            }), 400

        cursor.execute(
            """
            SELECT id_estado
            FROM estados_reporte
            WHERE nombre = 'recibido'
            """
        )

        estado = cursor.fetchone()

        if not estado:
            return jsonify({
                "error": "No está configurado el estado inicial del reporte"
            }), 500

        cursor.execute(
            """
            INSERT INTO reportes (
                folio,
                id_usuario,
                id_categoria,
                id_estado,
                titulo,
                descripcion,
                es_anonimo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                folio,
                usuario_id,
                id_categoria,
                estado["id_estado"],
                titulo,
                descripcion,
                es_anonimo,
            ),
        )

        id_reporte = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO credenciales_seguimiento (
                id_reporte,
                codigo_hash
            )
            VALUES (%s, %s)
            """,
            (id_reporte, codigo_hash),
        )

        # Guardar la ubicación textual si se proporcionó.
        if any(ubicacion.get(campo) for campo in campos_ubicacion):
            cursor.execute(
                """
                INSERT INTO ubicaciones (
                    id_reporte,
                    estado,
                    municipio,
                    colonia,
                    referencia
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    id_reporte,
                    ubicacion.get("estado"),
                    ubicacion.get("municipio"),
                    ubicacion.get("colonia"),
                    ubicacion.get("referencia"),
                ),
            )

        # Registrar el estado inicial en el historial.
        cursor.execute(
            """
            INSERT INTO historial_estados (
                id_reporte,
                id_estado_anterior,
                id_estado_nuevo,
                visible_reportante,
                comentario
            )
            VALUES (%s, NULL, %s, TRUE, %s)
            """,
            (
                id_reporte,
                estado["id_estado"],
                "Reporte recibido correctamente.",
            ),
        )

        connection.commit()

        return jsonify({
            "message": "Reporte registrado correctamente",
            "folio": folio,
            "codigo_seguimiento": codigo_privado,
            "advertencia": (
                "Guarda el folio y el código privado. "
                "El código no se volverá a mostrar."
            ),
        }), 201

    except Exception:
        if connection:
            connection.rollback()

        reportes_bp.logger.exception(
            "Error al registrar un reporte"
        )

        return jsonify({
            "error": "No fue posible registrar el reporte"
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@reportes_bp.post("/seguimiento/consultar")
def consultar_seguimiento():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Debes enviar los datos de consulta."
        }), 400

    folio = datos.get("folio")
    codigo = datos.get("codigo")

    if not isinstance(folio, str) or not isinstance(codigo, str):
        return jsonify({
            "error": "El folio y el código son obligatorios."
        }), 400

    folio = folio.strip().upper()
    codigo = codigo.strip()

    if not folio or not codigo:
        return jsonify({
            "error": "El folio y el código son obligatorios."
        }), 400

    if len(folio) > 40 or len(codigo) > 200:
        return jsonify({
            "error": "Los datos proporcionados no son válidos."
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Buscar el reporte y su credencial privada.
        cursor.execute("""
                SELECT
                    r.id_reporte,
                    r.folio,
                    r.titulo,
                    r.descripcion,
                    r.fecha_reporte,
                    r.fecha_actualizacion,
                    r.id_estado,
                    e.nombre AS estado,
                    e.descripcion AS descripcion_estado,
                    c.codigo_hash
                FROM reportes AS r
                INNER JOIN estados_reporte AS e
                    ON e.id_estado = r.id_estado
                INNER JOIN credenciales_seguimiento AS c
                    ON c.id_reporte = r.id_reporte
                WHERE r.folio = %s
                    AND c.revocada = 0
                    AND (
                       c.fecha_expiracion IS NULL
                       OR c.fecha_expiracion > NOW()
                    )
                LIMIT 1
            """, (folio,))

        reporte = cursor.fetchone()

        # Usar el mismo mensaje si el folio o el código no coinciden.
        if not reporte:
            return jsonify({
                "error": "No fue posible validar el folio y el código privado."
            }), 404

        # Calcular el hash del código recibido.
        codigo_hash = hashlib.sha256(
            codigo.encode("utf-8")
        ).hexdigest()

        # Comparar el hash recibido con el almacenado.
        if not hmac.compare_digest(
            reporte["codigo_hash"],
            codigo_hash
        ):
            return jsonify({
                "error": "No fue posible validar el folio y el código privado."
            }), 404

        # Consultar únicamente los movimientos visibles
        # para la persona que realizó el reporte.
        cursor.execute("""
            SELECT
                h.fecha_cambio,
                h.comentario,
                e.nombre AS estado
            FROM historial_estados AS h
            INNER JOIN estados_reporte AS e
                ON e.id_estado = h.id_estado_nuevo
            WHERE h.id_reporte = %s
              AND h.visible_reportante = 1
            ORDER BY h.fecha_cambio ASC
        """, (reporte["id_reporte"],))

        historial = cursor.fetchall()

        # Convertir las fechas a texto para enviarlas como JSON.
        for movimiento in historial:
            if movimiento["fecha_cambio"]:
                movimiento["fecha_cambio"] = (
                    movimiento["fecha_cambio"].isoformat()
                )

        return jsonify({
            "mensaje": "Reporte encontrado correctamente.",
            "reporte": {
                "folio": reporte["folio"],
                "titulo": reporte["titulo"],
                "descripcion": reporte["descripcion"],
                "estado": reporte["estado"],
                "descripcion_estado": reporte["descripcion_estado"],
                "fecha_reporte": (
                    reporte["fecha_reporte"].isoformat()
                    if reporte["fecha_reporte"] else None
                ),
                "fecha_actualizacion": (
                    reporte["fecha_actualizacion"].isoformat()
                    if reporte["fecha_actualizacion"] else None
                )
            },
            "historial": historial
        }), 200

    except Exception:
        current_app.logger.exception(
            "Error al consultar el seguimiento de un reporte"
        )

        return jsonify({
            "error": "Ocurrió un problema al consultar el reporte."
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()