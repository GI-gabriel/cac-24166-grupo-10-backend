
function iniciar() {
    var elemento = document.getElementById("menu-button");
    elemento.addEventListener("click", mostrarMenu);
}

function mostrarMenu() {
    var elemento = document.getElementById("main-nav-bar");
    elemento.style.height = elemento.style.height != "260px" ? "260px" : "0";

    let estado = elemento.style.height != "260px" ? true : false;
    anim_boton(estado);
}

const mql = window.matchMedia("(max-width: 992px)");
mql.onchange = (e) => {
    var elemento = document.getElementById("main-nav-bar");
    elemento.style.height = e.matches ? "0" : "auto";

    let estado = elemento.style.height != "260px" ? true : false;
    anim_boton(estado);
};

window.addEventListener("load", iniciar);

function anim_boton(estado) {
    var e2 = document.getElementById("nav-icon1");
    if (estado)
        e2.classList.remove('open');
    else
        e2.classList.add('open');
}