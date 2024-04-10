// Initialize the map
var map = L.map('map').setView([0, 0], 12); // Default view

L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

var previousLocation = null; // Variable to store the previous location

if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        function (position) {
            var latlng = [position.coords.latitude, position.coords.longitude];
            map.setView(latlng, 26);
            L.marker(latlng).addTo(map)
                .bindPopup("You are here!").openPopup();
            previousLocation = latlng; // Set initial location as previous location
        },
        function (error) {
            console.error("Error getting geolocation:", error.message);
        }
    );
} else {
    console.error("Geolocation is not supported by your browser");
}

setInterval(updateMap, 10000);

async function updateMap() {
    try {
        // Make a request to your API to fetch real-time location data
        const response = await fetch('/get_vehicle_location', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });


        const data = await response.json();
        const records = data.data;
        console.log(records)

        // Clear existing markers and polylines before adding new ones
        map.eachLayer(layer => {
            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
                map.removeLayer(layer);
            }
        });

        // Update the map markers with the new location data and add popups
        records.forEach(location => {
            var marker = L.marker([location.latitude, location.longitude]).addTo(map);
            var popupContent = `
                <strong>Latitude:</strong> ${location.latitude}<br>
                <strong>Longitude:</strong> ${location.longitude}<br>
                <strong>Time:</strong> ${location.gpstime}<br>
                <strong>Address:</strong> ${location.address}<br>
            `;
            marker.bindPopup(popupContent).openPopup();

            // Draw a polyline if there is a previous location
            if (previousLocation) {
                var polyline = L.polyline([previousLocation, [location.latitude, location.longitude]], { color: 'blue' }).addTo(map);
            }

            // Update the previous location
            previousLocation = [location.latitude, location.longitude];
        });

    } catch (error) {
        console.error('Error fetching real-time data', error);
    }
}
