function jumpTo(anchor) {
    document.getElementById(anchor).scrollIntoView();
}

/* Home page */

function addCoev() {
    document.getElementById("add-coev-form").style.display = "block";
    document.getElementById("add-curso-form").style.display = "none";
    document.getElementById("add-coev-btn").classList.add("active");
    document.getElementById("add-curso-btn").classList.remove("active");
}

function addCurso() {
    document.getElementById("add-coev-form").style.display = "none";
    document.getElementById("add-curso-form").style.display = "block";
    document.getElementById("add-coev-btn").classList.remove("active");
    document.getElementById("add-curso-btn").classList.add("active");
}

function cancelAdd() {
    document.getElementById("add-coev-form").style.display = "none";
    document.getElementById("add-curso-form").style.display = "none";
    document.getElementById("add-coev-btn").classList.remove("active");
    document.getElementById("add-curso-btn").classList.remove("active");
}

/* Perfil */

function showNotas(code) {
    let nr = document.getElementsByClassName("notas-resumen");
    let l = nr.length;
    for (let i = 0; i < l; i++) {
        nr[i].style.display = 'none';
    }
    document.getElementById("notas-resumen-"+code).style.display = "block";
    document.getElementById("notas-placeholder").style.display = "none";
    let active = document.getElementsByClassName("disp");
    let s = active.length;
    for (let i = 0; i < s; i++) {
        active[i].classList.remove("active");
    }
    document.getElementById("row-btn-"+code).classList.add("active");
}

/* Gestión Curso */

function seeCourse(year, semester, code, section) {
    let url = "http://127.0.0.1:8000/course/";
    let s = "/";
    url = url.concat(year, s, semester, s, code, s, section);
    window.location.href =(url);
}

function showGestionEstudiante() {
    document.getElementById("gestion-grupo").style.display = "none";
    document.getElementById("gestion-estudiante").style.display = "block";
    document.getElementById("gestion-placeholder").style.display = "none";
    document.getElementById("active-estudiante").classList.add("active");
    document.getElementById("active-grupo").classList.remove("active");
}

function showGestionGrupo() {
    document.getElementById("gestion-grupo").style.display = "block";
    document.getElementById("gestion-estudiante").style.display = "none";
    document.getElementById("gestion-placeholder").style.display = "none";
    document.getElementById("active-grupo").classList.add("active");
    document.getElementById("active-estudiante").classList.remove("active");
}


/* CoEvaluations */

function seeCoEv(id) {
    let url = "http://127.0.0.1:8000/coevaluation/";
    let s = "/";
    url = url.concat(id, s);
    window.location.href =(url);
}
function seeCoEv2(id_coev, id_st) {
    let url = "http://127.0.0.1:8000/coevaluation/";
    let s = "/";
    url = url.concat(id_coev, s, id_st,s);
    window.location.href =(url);
}
