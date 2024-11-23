function iniciar_mapa() {
	let coordenadas_centrales = {lat: -34.595657, lng: -58.451228};
	let mapa = new google.maps.Map(document.getElementById('map'), {zoom: 10, center: coordenadas_centrales});
	
	// console.log(latitud);
	// console.log(longitud);
	// let latitud_1 = parseFloat(latitud);
	// let longitud_1 = parseFloat(longitud);
	// console.log(latitud_1);
	// console.log(longitud_1);

	// let coordenada = { lat: latitud_1, lng: longitud_1};
	// let advancedMarker = new google.maps.Marker({position: coordenada, map: mapa});

	// console.log("Coordenadas del mapa:", coordenadas);

	coordenadas.forEach((coordenada, index) => {
        // console.log(`Creando marcador ${index + 1} en:`, coordenada);
        
        if (coordenada.lat && coordenada.lng) {
            new google.maps.Marker({
                position: { lat: coordenada.lat, lng: coordenada.lng },
                map: mapa,
            });
        } else {
            // console.warn(`Coordenada inválida en el índice ${index}:`, coordenada);
        }
    });

	let coordenada_hardcodeada = {lat: -34.590165, lng: -58.372720};
	let marcador_3 = new google.maps.Marker({position: coordenada_hardcodeada, map: mapa});
}	