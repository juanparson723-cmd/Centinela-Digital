import re

from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/registro")
def registrar_usuario():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Debes enviar los datos en formato JSON."
        }), 400

    nombre = datos.get("nombre")
    correo = datos.get("correo")
    contrasena = datos.get("contrasena")

    # Validar tipos de datos.
    if not all(isinstance(valor, str) for valor in (
        nombre, correo, contrasena
    )):
        return jsonify({
            "error": "Los datos enviados no tienen un formato válido."
        }), 400

    nombre = nombre.strip()
    correo = correo.strip().lower()

    # Validar campos vacíos.
    if not nombre or not correo or not contrasena:
        return jsonify({
            "error": "Todos los campos son obligatorios."
        }), 400

    # Validar longitudes.
    if len(nombre) > 100 or len(correo) > 150:
        return jsonify({
            "error": "El nombre o correo superan el tamaño permitido."
        }), 400

    if len(contrasena) < 8:
        return jsonify({
            "error": "La contraseña debe tener al menos 8 caracteres."
        }), 400

    if len(contrasena) > 1024:
        return jsonify({
            "error": "La contraseña es demasiado extensa."
        }), 400

    # Validar formato básico del correo.
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
        return jsonify({
            "error": "Ingresa un correo electrónico válido."
        }), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Comprobar si el correo ya está registrado.
        cursor.execute(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE correo = %s
            LIMIT 1
            """,
            (correo,)
        )

        if cursor.fetchone():
            return jsonify({
                "error": "Ya existe una cuenta con ese correo."
            }), 409

        # Buscar el rol ciudadano.
        cursor.execute(
            """
            SELECT id_rol
            FROM roles
            WHERE nombre = %s
            LIMIT 1
            """,
            ("ciudadano",)
        )

        rol = cursor.fetchone()

        if not rol:
            return jsonify({
                "error": "No está configurado el rol ciudadano."
            }), 500

        # Generar el hash de la contraseña.
        contrasena_hash = generate_password_hash(contrasena)

        # Registrar al usuario.
        cursor.execute(
            """
            INSERT INTO usuarios (
                id_rol,
                nombre,
                correo,
                contrasena_hash,
                activo
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                rol["id_rol"],
                nombre,
                correo,
                contrasena_hash,
                1
            )
        )

        connection.commit()

        return jsonify({
            "status": "ok",
            "message": "Cuenta creada correctamente."
        }), 201

    except Exception:
        if connection:
            connection.rollback()

        current_app.logger.exception(
            "Error al registrar un usuario."
        )

        return jsonify({
            "error": "No fue posible crear la cuenta."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@auth_bp.post("/login")
def login():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Debes enviar las credenciales en formato JSON."
        }), 400

    correo = datos.get("correo", "")
    contrasena = datos.get("contrasena", "")

    if not isinstance(correo, str) or not isinstance(contrasena, str):
        return jsonify({
            "error": "Las credenciales no tienen un formato válido."
        }), 400

    correo = correo.strip().lower()

    if not correo or not contrasena:
        return jsonify({
            "error": "Ingresa tu correo y contraseña."
        }), 400

    if len(correo) > 150 or len(contrasena) > 1024:
        return jsonify({
            "error": "Las credenciales superan el tamaño permitido."
        }), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
        return jsonify({
            "error": "Ingresa un correo electrónico válido."
        }), 400

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
                u.contrasena_hash,
                u.activo,
                r.nombre AS rol
            FROM usuarios AS u
            INNER JOIN roles AS r
                ON u.id_rol = r.id_rol
            WHERE LOWER(u.correo) = %s
            LIMIT 1
            """,
            (correo,)
        )

        usuario = cursor.fetchone()

        # Respuesta genérica para no revelar si existe el correo.
        if not usuario:
            return jsonify({
                "error": "Correo o contraseña incorrectos."
            }), 401

        if not usuario["activo"]:
            return jsonify({
                "error": "La cuenta está desactivada."
            }), 403

        if not check_password_hash(
            usuario["contrasena_hash"],
            contrasena
        ):
            return jsonify({
                "error": "Correo o contraseña incorrectos."
            }), 401

        # Crear una sesión nueva después de autenticar.
        session.clear()
        session.permanent = True

        session["usuario_id"] = usuario["id_usuario"]
        session["usuario_nombre"] = usuario["nombre"]
        session["usuario_rol"] = usuario["rol"]

        return jsonify({
            "status": "ok",
            "message": "Credenciales verificadas correctamente.",
            "usuario": {
                "id": usuario["id_usuario"],
                "nombre": usuario["nombre"],
                "correo": usuario["correo"],
                "rol": usuario["rol"]
            }
        }), 200

    except Exception:
        current_app.logger.exception(
            "Error al procesar el inicio de sesión."
        )

        return jsonify({
            "error": "No fue posible procesar el inicio de sesión."
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


@auth_bp.get("/me")
def usuario_actual():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({
            "autenticado": False,
            "error": "No hay una sesión activa."
        }), 401

    return jsonify({
        "autenticado": True,
        "usuario": {
            "id": usuario_id,
            "nombre": session.get("usuario_nombre"),
            "rol": session.get("usuario_rol")
        }
    }), 200


@auth_bp.post("/logout")
def logout():
    session.clear()

    return jsonify({
        "status": "ok",
        "message": "Sesión cerrada correctamente."
    }), 200