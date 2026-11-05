from getpass import getpass

from werkzeug.security import generate_password_hash

from database import get_connection


def crear_usuario():
    print("=== Crear usuario de prueba: Centinela Digital ===")

    nombre = input("Nombre del usuario: ").strip()
    correo = input("Correo electrónico: ").strip().lower()
    contrasena = getpass("Contraseña para la cuenta: ")

    if not nombre or not correo or not contrasena:
        print("Todos los campos son obligatorios.")
        return

    if len(nombre) > 100 or len(correo) > 150:
        print("El nombre o el correo superan el tamaño permitido.")
        return

    if len(contrasena) < 8:
        print("Utiliza una contraseña de al menos 8 caracteres.")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

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
            print(
                "No se encontró el rol 'usuario'. "
                "Revisa los registros de la tabla roles."
            )
            connection.rollback()
            return

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
            print("Ya existe una cuenta con ese correo.")
            connection.rollback()
            return

        contrasena_hash = generate_password_hash(contrasena)

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

        print("\nUsuario de prueba creado correctamente.")
        print(f"Correo: {correo}")
        print("La contraseña se guardó mediante un hash seguro.")

    except Exception as error:
        if connection is not None:
            connection.rollback()

        print(f"No fue posible crear el usuario: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__ == "__main__":
    crear_usuario()