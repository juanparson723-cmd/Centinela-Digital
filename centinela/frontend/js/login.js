document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario-login");
    const campoCorreo = document.getElementById("correo");
    const campoContrasena = document.getElementById("contrasena");
    const botonLogin = document.getElementById("boton-login");
    const mensajeLogin = document.getElementById("mensaje-login");

    if (!formulario) {
        console.error("No se encontró el formulario de inicio de sesión.");
        return;
    }

    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const correo = campoCorreo.value.trim();
        const contrasena = campoContrasena.value;

        if (!correo || !contrasena) {
            mostrarMensaje("Ingresa tu correo y contraseña.", "error");
            return;
        }

        botonLogin.disabled = true;
        botonLogin.textContent = "Iniciando sesión...";

        try {
            const respuesta = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "same-origin",
                body: JSON.stringify({
                    correo: correo,
                    contrasena: contrasena
                })
            });

            const datos = await respuesta.json();

            if (!respuesta.ok) {
                mostrarMensaje(
                    datos.error || datos.mensaje || "No se pudo iniciar sesión. Verifica tus credenciales.",
                    "error"
                );
                return;
            }

            mostrarMensaje("Inicio de sesión exitoso. Redirigiendo...", "exito");

            window.location.href = "/reporte";

        } catch (error) {
            console.error("Error al iniciar sesión:", error);
            mostrarMensaje(
                "No se pudo conectar con el servidor. Inténtalo de nuevo.",
                "error"
            );
        } finally {
            botonLogin.disabled = false;
            botonLogin.textContent = "Iniciar sesión";
        }
    });

    function mostrarMensaje(texto, tipo) {
        if (!mensajeLogin) {
            console.log(texto);
            return;
        }

        mensajeLogin.textContent = texto;
        mensajeLogin.classList.remove("error", "exito");
        mensajeLogin.classList.add(tipo);
    }
});
