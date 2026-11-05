
"use strict";

const formularioRegistro = document.getElementById(
    "formulario-registro"
);

const campoNombre = document.getElementById("nombre");
const campoCorreo = document.getElementById("correo");
const campoContrasena = document.getElementById("contrasena");

const campoConfirmar = document.getElementById(
    "confirmar-contrasena"
);

const botonRegistro = document.getElementById("boton-registro");
const mensajeRegistro = document.getElementById("mensaje-registro");


function mostrarMensaje(texto, tipo = "error") {
    mensajeRegistro.textContent = texto;
    mensajeRegistro.className = `mensaje ${tipo}`;
    mensajeRegistro.hidden = false;
}


formularioRegistro.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    mensajeRegistro.hidden = true;

    const nombre = campoNombre.value.trim();
    const correo = campoCorreo.value.trim().toLowerCase();
    const contrasena = campoContrasena.value;
    const confirmar = campoConfirmar.value;

    // Comprobar que las contraseñas coincidan.
    if (contrasena !== confirmar) {
        mostrarMensaje("Las contraseñas no coinciden.");
        return;
    }

    if (contrasena.length < 8) {
        mostrarMensaje(
            "La contraseña debe tener al menos 8 caracteres."
        );
        return;
    }

    const datos = {
        nombre: nombre,
        correo: correo,
        contrasena: contrasena
    };

    botonRegistro.disabled = true;
    botonRegistro.textContent = "Creando cuenta...";

    try {

        const respuesta = await fetch("/api/auth/registro", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            credentials: "same-origin",

            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json().catch(() => ({}));

        if (!respuesta.ok) {
            mostrarMensaje(
                resultado.error || "No fue posible crear la cuenta."
            );
            return;
        }

        mostrarMensaje(
            "¡Tu cuenta fue creada correctamente! Ahora puedes iniciar sesión.",
            "exito"
        );

        formularioRegistro.reset();

    } catch (error) {

        console.error("Error al registrar la cuenta:", error);

        mostrarMensaje(
            "No fue posible conectar con el servidor."
        );

    } finally {

        botonRegistro.disabled = false;
        botonRegistro.textContent = "Crear cuenta";

    }

});
