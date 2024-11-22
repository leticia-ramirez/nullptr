function iniciar_mapa() {
	let coordenadas_centrales = {lat: -34.595657, lng: -58.451228};
	let mapa = new google.maps.Map(document.getElementById('map'), {zoom: 10, center: coordenadas_centrales});

	// COORDENADAS HARDCODEADAS PARA PROBAR FUNCIONALIDAD

	let coordenada_1_hardcodeada = {lat: -34.617745,lng: -58.367399};
	let marcador_1 = new google.maps.Marker({position: coordenada_1_hardcodeada, map: mapa});
	let coordenada_2_hardcodeada = {lat: -34.588711,lng: -58.429723};
	let marcador_2 = new google.maps.Marker({position: coordenada_2_hardcodeada, map: mapa});
	let coordenada_3_hardcodeada = {lat: -34.590165,lng: -58.372720};
	let marcador_3 = new google.maps.Marker({position: coordenada_3_hardcodeada, map: mapa});
}

iniciar_mapa()

// function iniciar_mapa() {
//     var coordenadas_centrales = {lat: -34.595657, lng: -58.451228};
//     var mapa = new google.maps.Map(document.getElementById('map'), {
//         zoom: 10,
//         center: coordenadas_centrales
//     });

//     // Coordenadas de ejemplo
//     var coordenadas = [
//         {lat: -34.617745, lng: -58.367399},
//         {lat: -34.588711, lng: -58.429723},
//         {lat: -34.590165, lng: -58.372720}
//     ];

//     // Añadir marcadores al mapa
//     coordenadas.forEach(coordenada => {
//         new google.maps.Marker({
//             position: coordenada,
//             map: mapa
//         });
//     });
// }
