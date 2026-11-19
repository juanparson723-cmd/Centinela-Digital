

const botonMenu = document.getElementById("boton-menu");
const menuNavegacion = document.getElementById("menu-navegacion");

if (botonMenu && menuNavegacion) {

    botonMenu.addEventListener("click", () => {

        const abierto = menuNavegacion.classList.toggle("abierto");

        botonMenu.setAttribute("aria-expanded", abierto);
        botonMenu.setAttribute(
            "aria-label",
            abierto ? "Cerrar menú" : "Abrir menú"
        );

    });

    menuNavegacion.querySelectorAll("a").forEach(enlace => {

        enlace.addEventListener("click", () => {

            menuNavegacion.classList.remove("abierto");

            botonMenu.setAttribute("aria-expanded", "false");
            botonMenu.setAttribute("aria-label", "Abrir menú");

        });

    });

}


// ANIMACIONES DE APARICIÓN

const elementos = document.querySelectorAll(".elemento-aparece");

if ("IntersectionObserver" in window) {

    const observador = new IntersectionObserver((entradas, observer) => {

        entradas.forEach(entrada => {

            if (entrada.isIntersecting) {

                entrada.target.classList.add("visible");

                observer.unobserve(entrada.target);

            }

        });

    }, {
        threshold: 0.12
    });

    elementos.forEach(elemento => {
        observador.observe(elemento);
    });

} else {

    // Alternativa para navegadores antiguos.

    elementos.forEach(elemento => {
        elemento.classList.add("visible");
    });

}


function configurarCarrusel(
    pistaId,
    anteriorId,
    siguienteId,
    indicadoresId
) {

    const pista = document.getElementById(pistaId);
    const anterior = document.getElementById(anteriorId);
    const siguiente = document.getElementById(siguienteId);
    const contenedorIndicadores =
        document.getElementById(indicadoresId);

    if (!pista || !anterior || !siguiente || !contenedorIndicadores) {
        return;
    }

    const tarjetas = Array.from(pista.children);
    const indicadores =
        Array.from(contenedorIndicadores.children);

    let posicion = 0;

    function actualizarCarrusel() {

        pista.style.transform =
            `translateX(-${posicion * 100}%)`;

        indicadores.forEach((indicador, indice) => {

            indicador.classList.toggle(
                "activo",
                indice === posicion
            );

        });

    }

    function cambiarPosicion(nuevaPosicion) {

        posicion = (nuevaPosicion + tarjetas.length)
            % tarjetas.length;

        actualizarCarrusel();

    }

    anterior.addEventListener("click", () => {
        cambiarPosicion(posicion - 1);
    });

    siguiente.addEventListener("click", () => {
        cambiarPosicion(posicion + 1);
    });

    indicadores.forEach((indicador, indice) => {

        indicador.addEventListener("click", () => {
            cambiarPosicion(indice);
        });

    });

    actualizarCarrusel();

}


// CARRUSEL INFORMATIVO

configurarCarrusel(
    "pista-tarjetas",
    "anterior-tarjeta",
    "siguiente-tarjeta",
    "indicadores-tarjetas"
);


// CARRUSEL DE ESTADÍSTICAS

configurarCarrusel(
    "pista-graficas",
    "anterior-grafica",
    "siguiente-grafica",
    "indicadores-graficas"
);


