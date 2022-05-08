function generateMap(){
    var map = L.map('map').setView([57.688, 11.97], 13);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoibW90b25hdXRlbiIsImEiOiJjbDBmeGZ6MnUweDAyM2psZnVzaG5sMmVuIn0.t3aowppliwRaOcZSLb8CdA'
    }).addTo(map);

    return map;
}

$(document).ready(function() {
    var map = generateMap();
    var owner = "Simon";

    var socket = io();

    motorcycleIcon = L.icon({
        iconUrl: 'https://motonaut.se/static/images/motorcycleicon.svg',
        iconSize: [30, 30],
        popupAnchor: [-3, -76]
    });

    socket.on('location', function(message) {
        console.log(message);

        data = JSON.parse(message);

        console.log(data);

        L.marker([data.latitude, data.longitude], {icon : motorcycleIcon}).addTo(map);
    });
});