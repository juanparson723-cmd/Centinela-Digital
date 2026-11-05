
document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.getElementById(
        "formulario-seguimiento"
    );

    const boton = document.getElementById(
        "boton-seguimiento"
    );

    const mensaje = document.getElementById(
        "mensaje-seguimiento"
    );

    const resultado = document.getElementById(
        "resultado-seguimiento"
    );

    const listaHistorial = document.getElementById(
        "lista-historial"
    );


    function mostrarMensaje(texto, tipo = "error") {
        mensaje.textContent = texto;
        mensaje.className = `mensaje ${tipo}`;
        mensaje.hidden = false;
    }


    function formatearFecha(fecha) {
        if (!fecha) {
            return "No disponible";
        }

        const fechaConvertida = new Date(fecha);

        if (Number.isNaN(fechaConvertida.getTime())) {
            return "No disponible";
        }

        return fechaConvertida.toLocaleString("es-MX", {
            dateStyle: "long",
            timeStyle: "short"
        });
    }


    function mostrarHistorial(historial) {
        listaHistorial.replaceChildren();

        if (!historial || historial.length === 0) {
            const texto = document.createElement("p");
            texto.textContent = "No hay movimientos disponibles.";
            listaHistorial.appendChild(texto);
            return;
        }

        historial.forEach((movimiento) => {
            const elemento = document.createElement("article");

            elemento.className = "tarjeta";

            const estado = document.createElement("h3");
            estado.textContent = movimiento.estado;

            const fecha = document.createElement("p");
            fecha.textContent = formatearFecha(
                movimiento.fecha_cambio
            );

            const comentario = document.createElement("p");
            comentario.textContent =
                movimiento.comentario || "Sin comentarios adicionales.";

            elemento.append(estado, fecha, comentario);
            listaHistorial.appendChild(elemento);
        });
    }


    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        mensaje.hidden = true;
        resultado.hidden = true;

        boton.disabled = true;
        boton.textContent = "Consultando...";

        const folio = document.getElementById("folio").value.trim();
        const codigo = document.getElementById("codigo").value.trim();

        try {
            const respuesta = await fetch(
                "/api/seguimiento/consultar",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "same-origin",

                    body: JSON.stringify({
                        folio: folio,
                        codigo: codigo
                    })
                }
            );

            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(
                    datos.error || "No fue posible consultar el reporte."
                );
            }

            const reporte = datos.reporte;

            document.getElementById("resultado-folio").textContent =
                reporte.folio;

            document.getElementById("resultado-titulo").textContent =
                reporte.titulo;

            document.getElementById("resultado-descripcion").textContent =
                reporte.descripcion;

            document.getElementById("resultado-estado").textContent =
                reporte.estado;

            document.getElementById("resultado-descripcion-estado").textContent =
                reporte.descripcion_estado || "Sin descripción disponible.";

            document.getElementById("resultado-fecha").textContent =
                formatearFecha(reporte.fecha_reporte);

            document.getElementById("resultado-actualizacion").textContent =
                formatearFecha(reporte.fecha_actualizacion);

            mostrarHistorial(datos.historial);

            resultado.hidden = false;

            mostrarMensaje(
                "El reporte se consultó correctamente.",
                "exito"
            );

        } catch (error) {
            mostrarMensaje(error.message);
        } finally {
            boton.disabled = false;
            boton.innerHTML =
                'Consultar reporte <span aria-hidden="true">→</span>';
        }
    });

});
