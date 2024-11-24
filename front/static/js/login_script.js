if (typeof logged !== "undefined" && logged == "True") {
    localStorage.setItem("usuario", usuario);
}

let registro = localStorage.getItem("usuario");
let sesion_iniciada = Object.keys(registro).length !== 0; 
let sesion = {};
if (sesion_iniciada) sesion = JSON.parse(registro);

console.log(sesion)

let isesion = document.getElementById("isesion");
let registrarse = document.getElementById("registrarse");
let csesion = document.getElementById("csesion");
if (sesion_iniciada) {
    isesion.style.display = "none";
    registrarse.style.display = "none";
    csesion.style.display = "inline-block";
}
csesion.addEventListener("click", () => {
    localStorage.removeItem("usuario");
    sesion_iniciada = false;
    isesion.style.display = "inline-block";
    registrarse.style.display = "inline-block";
    csesion.style.display = "none";
});

try {
    let ID_usuario = document.getElementById("ID_usuario");
    if (sesion_iniciada) ID_usuario.value = sesion["ID_usuario"];
} catch (error) {
    
}