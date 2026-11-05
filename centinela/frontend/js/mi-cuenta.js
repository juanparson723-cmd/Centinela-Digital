
const datosCuenta = document.getElementById("datos-cuenta");
const listaReportes = document.getElementById("lista-reportes");
const mensajeCuenta = document.getElementById("mensaje-cuenta");
const botonCerrarSesion = document.getElementById("cerrar-sesion");

// Evitar que los datos de la base de datos se interpreten como HTML.
function escaparHTML(valor) {
    return String(valor ?? "").replace(/[&<>"']/g, caracter => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[caracter]);
}

// Consultar los datos de la cuenta.
async function cargarCuenta() {
    try {
        const respuesta = await fetch("/api/mi-cuenta", {
            credentials: "same-origin"
        });

        const datos = await respuesta.json();

        if (respuesta.status === 401) {
            window.location.href = "/login";
            return;
        }

        if (!respuesta.ok) {
            throw new Error(datos.error || "No se pudo cargar la cuenta.");
        }

        const usuario = datos.usuario;

        datosCuenta.innerHTML = `
            <p><strong>Nombre:</strong> ${escaparHTML(usuario.nombre)}</p>
            <p><strong>Correo:</strong> ${escaparHTML(usuario.correo)}</p>
            <p><strong>Rol:</strong> ${escaparHTML(usuario.rol)}</p>
            <p><strong>Fecha de registro:</strong>
                ${escaparHTML(usuario.fecha_creacion)}
            </p>
        `;

    } catch (error) {
        datosCuenta.textContent = error.message;
    }
}

// Consultar los reportes del usuario.
async function cargarReportes() {
    try {
        const respuesta = await fetch("/api/mis-reportes", {
            credentials: "same-origin"
        });

        const datos = await respuesta.json();

        if (respuesta.status === 401) {
            window.location.href = "/login";
            return;
        }

        if (!respuesta.ok) {
            throw new Error(datos.error || "No se pudieron cargar los reportes.");
        }

        if (!datos.reportes || datos.reportes.length === 0) {
            listaReportes.textContent = "Todavía no tienes reportes registrados.";
            return;
        }

        listaReportes.innerHTML = datos.reportes.map(reporte => `
            <article class="reporte-card">
                <h3>${escaparHTML(reporte.titulo)}</h3>

                <p><strong>Folio:</strong> ${escaparHTML(reporte.folio)}</p>
                <p><strong>Categoría:</strong> ${escaparHTML(reporte.categoria)}</p>
                <p><strong>Estado:</strong>
                    <span class="estado-reporte">
                        ${escaparHTML(reporte.estado)}
                    </span>
                </p>
                <p><strong>Fecha:</strong>
                    ${escaparHTML(reporte.fecha_reporte)}
                </p>

                <div class="reporte-acciones">
                    <button class="boton-ver"
                        data-accion="ver"
                        data-folio="${escaparHTML(reporte.folio)}">
                        Ver detalles
                    </button>

                    <button class="boton-editar"
                        data-accion="editar"
                        data-folio="${escaparHTML(reporte.folio)}">
                        Modificar
                    </button>

                    <button class="boton-eliminar"
                        data-accion="eliminar"
                        data-folio="${escaparHTML(reporte.folio)}">
                        Eliminar
                    </button>
                </div>

                <div id="detalle-${escaparHTML(reporte.folio)}"></div>

                <form class="formulario-edicion"
                    id="form-${escaparHTML(reporte.folio)}"
                    data-folio="${escaparHTML(reporte.folio)}">

                    <label>Nuevo título</label>
                    <input type="text" name="titulo" maxlength="150"
                        value="${escaparHTML(reporte.titulo)}" required>

                    <label>Nueva descripción</label>
                    <textarea name="descripcion" required>${escaparHTML(reporte.descripcion)}</textarea>

                    <button type="submit" class="boton-cuenta">
                        Guardar cambios
                    </button>
                </form>
            </article>
        `).join("");

    } catch (error) {
        listaReportes.textContent = error.message;
    }
}

// Consultar un reporte individual.
async function verReporte(folio) {
    const contenedor = document.getElementById(`detalle-${folio}`);

    try {
        const respuesta = await fetch(
            `/api/mis-reportes/${encodeURIComponent(folio)}`,
            { credentials: "same-origin" }
        );

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.error || "No se pudo consultar el reporte.");
        }

        const reporte = datos.reporte;

        contenedor.innerHTML = `
            <div class="cuenta-panel">
                <h4>Detalles del reporte</h4>
                <p><strong>Descripción:</strong>
                    ${escaparHTML(reporte.descripcion)}
                </p>
                <p><strong>Estado:</strong>
                    ${escaparHTML(reporte.estado)}
                </p>
                <p><strong>Fecha de actualización:</strong>
                    ${escaparHTML(reporte.fecha_actualizacion)}
                </p>
            </div>
        `;

    } catch (error) {
        contenedor.textContent = error.message;
    }
}

// Mostrar u ocultar el formulario de modificación.
function mostrarEdicion(folio) {
    const formulario = document.getElementById(`form-${folio}`);

    if (formulario) {
        formulario.classList.toggle("activo");
    }
}

// Modificar un reporte.
async function guardarCambios(formulario) {
    const folio = formulario.dataset.folio;
    const boton = formulario.querySelector("button[type='submit']");

    const datos = {
        titulo: formulario.elements.titulo.value,
        descripcion: formulario.elements.descripcion.value
    };

    boton.disabled = true;
    boton.textContent = "Guardando...";

    try {
        const respuesta = await fetch(
            `/api/mis-reportes/${encodeURIComponent(folio)}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "same-origin",
                body: JSON.stringify(datos)
            }
        );

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(resultado.error || "No se pudieron guardar los cambios.");
        }

        mensajeCuenta.textContent = resultado.message;
        formulario.classList.remove("activo");

        await cargarReportes();

    } catch (error) {
        mensajeCuenta.textContent = error.message;

    } finally {
        boton.disabled = false;
        boton.textContent = "Guardar cambios";
    }
}

// Eliminar lógicamente un reporte.
async function eliminarReporte(folio) {
    const confirmar = confirm(
        `¿Estás seguro de que deseas eliminar el reporte ${folio}?`
    );

    if (!confirmar) return;

    try {
        const respuesta = await fetch(
            `/api/mis-reportes/${encodeURIComponent(folio)}`,
            {
                method: "DELETE",
                credentials: "same-origin"
            }
        );

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(resultado.error || "No se pudo eliminar el reporte.");
        }

        mensajeCuenta.textContent = resultado.message;
        await cargarReportes();

    } catch (error) {
        mensajeCuenta.textContent = error.message;
    }
}

// Detectar los botones de cada reporte.
listaReportes.addEventListener("click", event => {
    const boton = event.target.closest("button[data-accion]");

    if (!boton) return;

    const folio = boton.dataset.folio;
    const accion = boton.dataset.accion;

    if (accion === "ver") {
        verReporte(folio);
    }

    if (accion === "editar") {
        mostrarEdicion(folio);
    }

    if (accion === "eliminar") {
        eliminarReporte(folio);
    }
});

// Detectar el envío de los formularios de edición.
listaReportes.addEventListener("submit", event => {
    if (!event.target.matches(".formulario-edicion")) return;

    event.preventDefault();
    guardarCambios(event.target);
});

// Cerrar sesión.
botonCerrarSesion.addEventListener("click", async () => {
    try {
        const respuesta = await fetch("/api/auth/logout", {
            method: "POST",
            credentials: "same-origin"
        });

        if (!respuesta.ok) {
            throw new Error("No se pudo cerrar la sesión.");
        }

        window.location.href = "/login";

    } catch (error) {
        mensajeCuenta.textContent = error.message;
    }
});

// Cargar la información al abrir la página.
cargarCuenta();
cargarReportes();
