const tiposViolencia = {

    "familiar": {
        titulo: "Violencia familiar",
        descripcion:
            "Información y novedades relacionadas con situaciones de violencia dentro del entorno familiar.",
        noticias: []
    },

    "femenina": {
        titulo: "Violencia femenina",
        descripcion:
            "Información y novedades relacionadas con la prevención y atención de la violencia contra las mujeres.",
        noticias: []
    },

    "abuso-infantil": {
        titulo: "Abuso infantil",
        descripcion:
            "Información relacionada con la prevención y protección de niñas, niños y adolescentes.",
        noticias: []
    },

    "acoso-sexual": {
        titulo: "Acoso sexual",
        descripcion:
            "Información y novedades relacionadas con la prevención y atención del acoso sexual.",
        noticias: []
    },

    "acoso-laboral": {
        titulo: "Acoso laboral",
        descripcion:
            "Información relacionada con situaciones de hostigamiento y violencia en el entorno laboral.",
        noticias: []
    },

    "acoso-escolar": {
        titulo: "Acoso escolar",
        descripcion:
            "Información y novedades relacionadas con la prevención del acoso en el entorno educativo.",
        noticias: []
    }

};

const rutaActual = window.location.pathname;
const tipoActual = rutaActual.split("/").filter(Boolean).pop();

const informacion = tiposViolencia[tipoActual];

const titulo = document.getElementById("titulo-tipo");
const descripcion = document.getElementById("descripcion-tipo");
const listaNoticias = document.getElementById("lista-noticias");

if (informacion) {

    document.title =
        `Centinela Digital | ${informacion.titulo}`;

    titulo.textContent = informacion.titulo;
    descripcion.textContent = informacion.descripcion;

    if (informacion.noticias.length === 0) {

        listaNoticias.innerHTML = `
            <p class="estado-noticias">
                Próximamente se agregarán noticias y novedades
                verificadas para esta categoría.
            </p>
        `;

    }

} else {

    titulo.textContent = "Categoría no encontrada";

    descripcion.textContent =
        "No se encontró la categoría solicitada.";

    listaNoticias.innerHTML = `
        <p class="estado-noticias">
            La categoría solicitada no está disponible.
        </p>
    `;

}