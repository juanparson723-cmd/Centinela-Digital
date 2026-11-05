"use strict";

const formularioReporte = document.getElementById("formulario-reporte");
const selectorCategoria = document.getElementById("id_categoria");
const mensajeReporte = document.getElementById("mensaje-reporte");
const botonReporte = document.getElementById("boton-reporte");
const resultadoReporte = document.getElementById("resultado-reporte");

const campoFolio = document.getElementById("folio-generado");
const campoCodigo = document.getElementById("codigo-generado");
const botonCopiar = document.getElementById("copiar-credenciales");


function mostrarMensajeReporte(texto, tipo = "error") {
    mensajeReporte.textContent = texto;
    mensajeReporte.className = `mensaje ${tipo}`;
    mensajeReporte.hidden = false;
}


async function cargarCategorias() {
    try {
        const respuesta = await fetch("/api/categorias");
        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.error || "No se pudieron cargar las categorías.");
        }

        selectorCategoria.replaceChildren();

        const opcionInicial = document.createElement("option");
        opcionInicial.value = "";
        opcionInicial.textContent = "Selecciona una categoría";
        selectorCategoria.appendChild(opcionInicial);

        const categorias = Array.isArray(datos)
            ? datos
            : datos.categorias;

        if (!Array.isArray(categorias) || categorias.length === 0) {
            selectorCategoria.replaceChildren();

            const opcionVacia = document.createElement("option");
            opcionVacia.value = "";
            opcionVacia.textContent = "No hay categorías disponibles";
            selectorCategoria.appendChild(opcionVacia);

            mostrarMensajeReporte(
                "No hay categorías registradas. Revisa la tabla categorias_violencia."
            );

            return;
        }

        categorias.forEach((categoria) => {
            const opcion = document.createElement("option");

            opcion.value = categoria.id_categoria;
            opcion.textContent = categoria.nombre;

            selectorCategoria.appendChild(opcion);
        });

    } catch (error) {
        console.error("Error cargando categorías:", error);

        selectorCategoria.replaceChildren();

        const opcionError = document.createElement("option");
        opcionError.value = "";
        opcionError.textContent = "Error al cargar categorías";

        selectorCategoria.appendChild(opcionError);

        mostrarMensajeReporte(
            "No se pudieron cargar las categorías. Comprueba la conexión con el servidor."
        );
    }
}


formularioReporte.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    mensajeReporte.hidden = true;
    resultadoReporte.hidden = true;

    const datos = {
        titulo: document.getElementById("titulo").value.trim(),
        descripcion: document.getElementById("descripcion").value.trim(),
        id_categoria: Number(selectorCategoria.value),
        es_anonimo: document.getElementById("es_anonimo").checked,
        ubicacion: {
            estado: document.getElementById("estado").value.trim(),
            municipio: document.getElementById("municipio").value.trim(),
            colonia: document.getElementById("colonia").value.trim(),
            referencia: document.getElementById("referencia").value.trim()
        }
    };

    if (
        !datos.titulo ||
        datos.descripcion.length < 10 ||
        !Number.isInteger(datos.id_categoria) ||
        datos.id_categoria <= 0
    ) {
        mostrarMensajeReporte(
            "Completa el título, la descripción y selecciona una categoría válida."
        );
        return;
    }

    botonReporte.disabled = true;
    botonReporte.textContent = "Registrando reporte...";

    try {
        const respuesta = await fetch("/api/reportes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "same-origin",
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json().catch(() => ({}));

        if (!respuesta.ok) {
            mostrarMensajeReporte(
                resultado.error ||
                resultado.message ||
                "No fue posible registrar el reporte."
            );
            return;
        }

        const codigoSeguimiento =
            resultado.codigo_privado ?? resultado.codigo_seguimiento;

        if (!resultado.folio || !codigoSeguimiento) {
            mostrarMensajeReporte(
                "El reporte pudo haberse registrado, pero el servidor no devolvió las credenciales esperadas. Comprueba el resultado antes de volver a enviarlo."
            );
            return;
        }

campoFolio.value = resultado.folio;
campoCodigo.value = codigoSeguimiento;

        formularioReporte.hidden = true;
        resultadoReporte.hidden = false;

        mostrarMensajeReporte(
            "El reporte se registró correctamente. Guarda el folio y el código privado.",
            "exito"
        );

    } catch (error) {
        console.error("Error registrando reporte:", error);

        mostrarMensajeReporte(
            "No se pudo conectar con el servidor. Inténtalo nuevamente."
        );

    } finally {
        botonReporte.disabled = false;
        botonReporte.innerHTML = 'Enviar reporte <span aria-hidden="true">→</span>';
    }
});


botonCopiar.addEventListener("click", async () => {
    const credenciales =
        `Folio: ${campoFolio.value}\nCódigo privado: ${campoCodigo.value}`;

    try {
        await navigator.clipboard.writeText(credenciales);

        botonCopiar.textContent = "Credenciales copiadas";

    } catch {
        mostrarMensajeReporte(
            "No se pudieron copiar automáticamente. Selecciona los campos y copia sus valores."
        );
    }
});


cargarCategorias();