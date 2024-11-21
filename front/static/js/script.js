// select relacionados

const selectProvincias=document.getElementById('provincia');
const selectMunicipios= document.getElementById('municipio');
const selectLocalidades=document.getElementById('localidad');
function provincia(){
    fetch("https://apis.datos.gob.ar/georef/api/provincias?orden=nombre")
    .then(res=> res.ok ? res.json() : Promise.reject(res))
    .then(json=>{
        let options=`<option value="Elige una provincia">Elige una provincia</option>`;
        json.provincias.forEach(el => options +=`<option value="${el.nombre}">${el.nombre}</option>`);
        selectProvincias.innerHTML= options;

    })
    
}
document.addEventListener("DOMContentLoaded", provincia)

function municipio(provincia){
    fetch(`https://apis.datos.gob.ar/georef/api/municipios?provincia=${provincia}&orden=nombre&max=200`)
    .then(res=> res.ok ? res.json() : Promise.reject(res))
    .then(json=>{
        let options=`<option value="Elige un municipio">Elige un municipio</option>`;
        console.log(json.municipios)
        json.municipios.forEach(el => options +=`<option value="${el.nombre}">${el.nombre}</option>`);
        selectMunicipios.innerHTML= options;
    })
}
selectProvincias.addEventListener("change", el=>{
    municipio(el.target.value);
    console.log(el.target.value);
})

function localidad(municipio){
    fetch(`https://apis.datos.gob.ar/georef/api/localidades?municipio=${municipio}&orden=nombre&max=200`)
    .then(res=> res.ok ? res.json() : Promise.reject(res))
    .then(json=>{
        let options=`<option value="Elige una localidad">Elige una localidad</option>`;
        
        json.localidades.forEach(el => options +=`<option value="${el.nombre}">${el.nombre}</option>`);
        selectLocalidades.innerHTML = options;
    })
}
selectMunicipios.addEventListener("change", el=>{
    localidad(el.target.value);
    console.log(el.target.value);
    console.log(el);
})