import os

from dotenv import load_dotenv
from mysql.connector import pooling

# Cargar las variables de entorno desde la raíz del proyecto.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

db_pool = pooling.MySQLConnectionPool(
    pool_name="centinela_pool",
    pool_size=5,
    pool_reset_session=True,
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "centinela_digital"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    autocommit=False,
)


def get_connection():
    """Obtiene una conexión disponible del grupo de conexiones."""
    return db_pool.get_connection()


def test_connection():
    """Comprueba la conexión con MySQL y devuelve su versión."""
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT VERSION() AS version")
        result = cursor.fetchone()

        return result["version"]

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()