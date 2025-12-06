var map = L.map('map').setView([17.385, 78.486], 14);

// Online OSM tiles (will replace with offline later)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

let startMarker, endMarker, routeLine;
let userMarker = null; // live movement marker

//----------------------------------------------
// 🟢 LIVE GPS TRACKING (Updates coordinates on screen)
//----------------------------------------------
navigator.geolocation.watchPosition(
    pos => {
        let lat = pos.coords.latitude;
        let lon = pos.coords.longitude;

        // Update coordinate box
        document.getElementById("coords-box").innerHTML =
            `Lat: ${lat.toFixed(6)} <br> Lon: ${lon.toFixed(6)}`;

        if (!userMarker) {
            // First time → place marker
            userMarker = L.marker([lat, lon], { 
                title: "You"
            }).addTo(map);

            map.setView([lat, lon], 16);  // Center map on first GPS fix
        } else {
            // Update marker as you walk
            userMarker.setLatLng([lat, lon]);
        }

        console.log("Live position:", lat, lon);
    },
    err => {
        console.log("GPS Error:", err);
    },
    {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 1000
    }
);

//----------------------------------------------
// 🟦 CLICK EVENT → Calculate walking route
//----------------------------------------------
map.on('click', function (e) {
    navigator.geolocation.getCurrentPosition(pos => {
        let start = {
            lat: pos.coords.latitude,
            lon: pos.coords.longitude
        };

        let end = {
            lat: e.latlng.lat,
            lon: e.latlng.lng
        };

        if (startMarker) map.removeLayer(startMarker);
        if (endMarker) map.removeLayer(endMarker);
        if (routeLine) map.removeLayer(routeLine);

        startMarker = L.marker([start.lat, start.lon]).addTo(map);
        endMarker = L.marker([end.lat, end.lon]).addTo(map);

        getRoute(start, end);
    });
});

//----------------------------------------------
// 🟨 FETCH ROUTE (via Flask → OSRM online)
//----------------------------------------------
function getRoute(start, end) {
    fetch("/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start, end })
    })
        .then(res => res.json())
        .then(json => {
            let encoded = json.routes[0].geometry;
            let coords = decode(encoded);

            routeLine = L.polyline(coords, { color: "blue", weight: 5 }).addTo(map);
            map.fitBounds(routeLine.getBounds());
        });
}

//----------------------------------------------
// 🔵 POLYLINE DECODER (OSRM geometry)
//----------------------------------------------
function decode(str) {
    let index = 0, lat = 0, lng = 0, coords = [];

    while (index < str.length) {
        let b, shift = 0, result = 0;
        do { 
            b = str.charCodeAt(index++) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);

        let dlat = (result & 1) ? ~(result >> 1) : (result >> 1);
        lat += dlat;

        shift = 0;
        result = 0;
        do {
            b = str.charCodeAt(index++) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);

        let dlng = (result & 1) ? ~(result >> 1) : (result >> 1);
        lng += dlng;

        coords.push([lat / 1e5, lng / 1e5]);
    }

    return coords;
}
