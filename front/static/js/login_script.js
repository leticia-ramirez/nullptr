if (typeof logged !== "undefined" && logged == "True") {
    localStorage.setItem("usuario", usuario);
    window.location.replace("http://127.0.0.1:5001/")
}

let registro = localStorage.getItem("usuario");
let sesion_iniciada = registro != null && Object.keys(registro).length !== 0; 
let sesion = {};
let pagina = document.title.split("|")[1].trim()
if (sesion_iniciada) sesion = JSON.parse(registro);

console.log(pagina)

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
    window.location.replace("http://127.0.0.1:5001/");
});

try {
    let ID_usuario = document.getElementById("ID_usuario");
    if (sesion_iniciada) ID_usuario.value = sesion["ID_usuario"];
} catch (error) {
    
}

switch(pagina) {
    case "Mis Reportes":
        let alert = document.getElementById("login-alert");
        if (!sesion_iniciada) alert.innerHTML = "¡Inicie sesion para ver sus reportes!";
        if(window.location.href.split("/").slice(-1) == "misreportes" && sesion_iniciada) {
            window.location.replace("misreportes/usuario/" + sesion["ID_usuario"])
        };
        break;
    case "Nuevo Reporte":
        let alertn = document.getElementById("login-alert")
        if (!sesion_iniciada) {
            alertn.innerHTML = "¡Inicie sesion para subir un reporte!";
            alertn.hidden = false;
            let form = document.getElementById("content");
            form.hidden = true;
        }
}