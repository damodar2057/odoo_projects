// Initialize the map
var map = L.map('map').setView([27.651759, 85.327921], 13);

L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

var warehouseMarker;
var destinationMarker;
var vehicleMarker;
var routePolyline; // Declare routePolyline variable

// Function to add a marker to the map with a custom icon
function addMarker(latlng, label, iconPath) {
    var customIcon = L.icon({
        iconUrl: iconPath,
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        popupAnchor: [0, -16],
    });

    var marker = L.marker(latlng, { icon: customIcon }).addTo(map);

    if (label) {
        marker.bindPopup(label);
    }

    return marker;
}

// Function to fetch and display initial coordinates and draw route
async function initialMap() {
    try {
        const response = await fetch('/get_initial_coordinates', {
            method: 'GET',
        });

        const data = await response.json();

        const sourceLocation = data.data.source_location;
        const destinationLocation = data.data.destination_location;
        const assignedVehicleLocation = data.data.assigned_vehicle_current_coordinates;

        // Add markers for each location
        warehouseMarker = addMarker(
            [sourceLocation.latitude, sourceLocation.longitude],
            'Source Location',
            'vehicle_tracking/static/description/warehouse_icon.png'
        );
        destinationMarker = addMarker(
            [destinationLocation.latitude, destinationLocation.longitude],
            'Destination Location',
            'vehicle_tracking/static/description/house.png'
        );
        vehicleMarker = addMarker(
            [assignedVehicleLocation.latitude, assignedVehicleLocation.longitude],
            'Assigned Vehicle Location',
            'vehicle_tracking/static/description/vehicle.png'
        );

        // Fetch driving route from warehouse to destination using OpenRouteService
        const routeResponse = await fetch(
            `https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248a0ed457aaf4242328297a7ea5dce7e06&start=${sourceLocation.longitude},${sourceLocation.latitude}&end=${destinationLocation.longitude},${destinationLocation.latitude}`
        );
        console.log(routeResponse)

        if (!routeResponse.ok) {
            throw new Error('Failed to fetch route data');
        }

        const routeData = await routeResponse.json();

        if (!routeData.features || routeData.features.length === 0) {
            throw new Error('No route data found');
        }

        // Extract route coordinates
        const routeCoordinates = routeData.features[0].geometry.coordinates;
        console.log(routeCoordinates)

        // Remove existing route polyline if it exists
        if (routePolyline) {
            map.removeLayer(routePolyline);
        }
        // Convert coordinates to [latitude, longitude] format
        var correctedCoordinates = routeCoordinates.map(function(coord) {
            return [coord[1], coord[0]];
        });
        console.log(correctedCoordinates)

//
//        // Draw a route polyline from warehouse to destination
//        routePolyline = L.Routing.control({
//            waypoints: [
//                L.latLng(sourceLocation.latitude, sourceLocation.longitude),
//                L.latLng(destinationLocation.latitude, destinationLocation.longitude)
//            ],
//            routeWhileDragging: true
//        }).addTo(map);
//
//        // Add the polyline to the map
//        routePolyline.on('routeselected', function (e) {
//            var route = e.route;
//            L.geoJSON(route.geometry, {
//                style: function () {
//                    return { color: '#007BFF', weight: 4, opacity: 0.8 };
//                }
//            }).addTo(map);
//        });

        // Draw a route polyline from warehouse to destination
          var polyline = L.polyline(correctedCoordinates, {
            color: '#007BFF', // Blue color
            weight: 4,
            opacity: 0.8
        }).addTo(map);
            } catch (error) {
                console.error('Error fetching or displaying data:', error);
            }
        }


// Function to fetch and update vehicle coordinates
async function updateVehicleInMap() {
    try {
        const response = await fetch('/update_assigned_vehicle_location', {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error('Failed to fetch vehicle data');
        }

        // Remove existing vehicle marker if it exists
        if (map.hasLayer(vehicleMarker) || map.hasLayer(newMarker)) {
            map.removeLayer(vehicleMarker);
        }

        const data = await response.json(); // Parse JSON response

        // Extract data from the response
        const vehicleCurrentLocation = data.data[0];
        console.log(vehicleCurrentLocation.latitude);

        // Update the vehicle marker with the new coordinates and custom icon
        vehicleMarker = addMarker(
            [vehicleCurrentLocation.latitude, vehicleCurrentLocation.longitude],
            'Assigned Vehicle Location',
            'vehicle_tracking/static/description/vehicle.png'
        );

    } catch (error) {
        console.error('Error fetching or updating vehicle data:', error);
    }
}

// Initial setup
initialMap();

// Update vehicle location every 15 seconds
setInterval(updateVehicleInMap, 15000);
