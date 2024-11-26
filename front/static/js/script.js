/*
 *  Pre: Escucha que se lleno las direcciones del formulario.
 *  Post: Muestra un Pop-Up con un mapa esperando la confirmacion de que la
 *       ubicacion ingresada es la correcta.
 */
document.addEventListener("DOMContentLoaded", () => {
    const direccionInput = document.getElementById("direccion");
    const modal = document.getElementById("confirmationModal");
    const closeModal = document.getElementById("closeModal");
    const confirmBtn = document.getElementById("confirmBtn");
    const cancelBtn = document.getElementById("cancelBtn");

    direccionInput.addEventListener("change", async () => {
        const provincia = document.getElementById("provincia").value;
        const municipio = document.getElementById("municipio").value;
        const localidad = document.getElementById("localidad").value;
        const direccion = direccionInput.value;

        if (direccion && provincia && localidad) {
            try {
                const response = await fetch(`/get_coordinates?provincia=${provincia}&municipio=${municipio}&localidad=${localidad}&direccion=${direccion}`);
                if (!response.ok) {
                    throw new Error("Error al obtener las coordenadas. Verifique los datos ingresados.");
                }
                const data = await response.json();
                if (data.lat && data.lon) {
                    showMap(data.lat, data.lon);
                    modal.style.display = "block";
                } else {
                    alert("No se encontraron coordenadas para esta dirección. Verifique los datos.");
                }
            } catch (error) {
                console.error(error);
                alert("Error al obtener las coordenadas. Intente nuevamente.");
            }
        } else {
            alert("Por favor, complete todos los campos antes de continuar.");
        }
    });

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    cancelBtn.addEventListener("click", () => {
        modal.style.display = "none";
        alert("Por favor, corrija la dirección ingresada.");
        direccionInput.focus();
    });

    confirmBtn.addEventListener("click", () => {
        modal.style.display = "none";
        alert("Dirección confirmada.");
    });

    function showMap(lat, lon) {
        const mapElement = document.getElementById("map");
        if (!mapElement) {
            console.error("El elemento del mapa no existe.");
            return;
        }
        const map = new google.maps.Map(mapElement, {
            center: { lat: lat, lng: lon },
            zoom: 15,
        });
        new google.maps.Marker({
            position: { lat: lat, lng: lon },
            map: map,
        });
    }
});


/*
 *  Pre: Escucha que se quiso enviar el formulario.
 *  Post: Muestra un alert y despues envia el formulario.
 */
document.getElementById('mi_formulario').addEventListener('submit', function(event) {
    alert('Formulario enviado con éxito');
    this.submit();
});


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
})
