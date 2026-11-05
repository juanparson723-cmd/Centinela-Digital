import os

from datetime import timedelta
from flask import (
    Flask,
    jsonify,
    send_from_directory,
)
from dotenv import load_dotenv

from database import test_connection
from routes.auth import auth_bp
from routes.reportes import reportes_bp
from routes.cuenta import cuenta_bp


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")

load_dotenv(os.path.join(PROJECT_DIR, ".env"))

app = Flask(__name__)

secret_key = os.getenv("FLASK_SECRET_KEY")

if not secret_key:
    raise RuntimeError(
        "Debes configurar FLASK_SECRET_KEY en el archivo .env"
    )

app.config.update(
    SECRET_KEY=secret_key,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=(
        os.getenv("COOKIE_SECURE", "false").lower() == "true"
    ),
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2),
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,
)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(reportes_bp, url_prefix="/api")
app.register_blueprint(cuenta_bp, url_prefix="/api")

# Página principal: creación de cuenta.
@app.get("/")
def pagina_registro():
    return send_from_directory(FRONTEND_DIR, "registro.html")


# Página de inicio de sesión.
@app.get("/login")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


# Formulario de reportes.
@app.get("/reporte")
def pagina_reporte():
    return send_from_directory(FRONTEND_DIR, "reporte.html")

# Página para consultar el seguimiento de un reporte.
@app.get("/seguimiento")
def pagina_seguimiento():
    return send_from_directory(
        FRONTEND_DIR,
        "seguimiento.html"
    )

@app.route("/mi-cuenta")
def pagina_mi_cuenta():
    return send_from_directory(FRONTEND_DIR, "mi-cuenta.html")


# Archivos CSS y JavaScript.
@app.get("/css/<path:filename>")
def archivos_css(filename):
    return send_from_directory(
        os.path.join(FRONTEND_DIR, "css"),
        filename,
    )


@app.get("/js/<path:filename>")
def archivos_js(filename):
    return send_from_directory(
        os.path.join(FRONTEND_DIR, "js"),
        filename,
    )


# Comprobación de Flask y MySQL.
@app.get("/api/health")
def health():
    try:
        version = test_connection()

        return jsonify({
            "status": "ok",
            "message": "Backend y MySQL conectados correctamente",
            "database_version": version,
        }), 200

    except Exception:
        app.logger.exception(
            "Error al comprobar la conexión con MySQL"
        )

        return jsonify({
            "status": "error",
            "message": "No fue posible conectar con la base de datos",
        }), 503


@app.errorhandler(404)
def not_found(_error):
    return jsonify({
        "error": "Recurso no encontrado"
    }), 404


@app.errorhandler(413)
def payload_too_large(_error):
    return jsonify({
        "error": "El contenido enviado supera el tamaño permitido"
    }), 413


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({
        "error": "Error interno del servidor"
    }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )