let mapa, ubicacion_actual;

function iniciar_mapa() {
	let coordenadas_centrales = { lat: -34.595657, lng: -58.451228 };
    mapa = new google.maps.Map(document.getElementById("map"), {zoom: 15, center: coordenadas_centrales});
     
    let icono_customizado = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 10,
        fillColor: "#08cf3d",
        fillOpacity: 0.8,
        strokeWeight: 2,
        strokeColor: "#12421f",
    };

    let icono_incidencias = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 10,
        fillColor: "#e00934",
        fillOpacity: 0.8,
        strokeWeight: 2,
        strokeColor: "#851027",
    };

    ubicacion_actual = new google.maps.Marker({
        position: coordenadas_centrales,
        map: mapa,
        icon: icono_customizado,
        title: "Tu ubicación actual",
    });

    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(
        actualizar_posicion,
        recibir_error,
        { enableHighAccuracy: true, maximumAge: 0 }
        );
    } else {
        alert("La geolocalización no está soportada por tu navegador.");
    }

    coordenadas.forEach((coordenada, index) => {
        if (coordenada.lat && coordenada.lng) {
            new google.maps.Marker({
                position: { lat: coordenada.lat, lng: coordenada.lng },
                map: mapa,
                icon: icono_incidencias,
            });
        }
    });
}

function actualizar_posicion(position) {
    let { latitude, longitude } = position.coords;
    let nueva_posicion = { lat: latitude, lng: longitude };

    ubicacion_actual.setPosition(nueva_posicion);
    mapa.setCenter(nueva_posicion);
}

function recibir_error(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("Permiso denegado para acceder a la ubicación.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Información de ubicación no disponible.");
            break;
        case error.TIMEOUT:
            alert("Tiempo de espera agotado al intentar obtener la ubicación.");
            break;
        default:
            alert("Error desconocido al intentar acceder a la ubicación.");
    }
}
