odoo.define('vehicle_tracking.leaflet_initialization', function (require) {
    'use strict';
var map = null;
var marker = null;
var leafletCallback = null;

    var initializeCommonLeafletMap = function (mapContainerId) {
        var leafletCssLink = document.createElement('link');
        leafletCssLink.rel = 'stylesheet';
        leafletCssLink.href = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css';
        leafletCssLink.async = true;
        document.head.appendChild(leafletCssLink);

        var leafletScript = document.createElement('script');
        leafletScript.src = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js';
        leafletScript.async = true;

        leafletScript.onload = function () {
            // Initialize Leaflet map
            map = initializeMap(mapContainerId);
            if (leafletCallback) {
                leafletCallback();
            }
        };

        document.head.appendChild(leafletScript);
    };

    var initializeMap = function (mapContainerId) {
      var  newmap = L.map(mapContainerId).setView([27.700622439976943, 85.33366713333177], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(newmap);
        return newmap;
    };

    var pointMarker = function (lat, lng) {
        if (!marker) {
            marker = L.marker([lat, lng]).addTo(map);
        } else {
            map.removeLayer(marker);
            marker = L.marker([lat, lng]).addTo(map);
        }
    };

    var pointVehicles= function (lat,lng){
        var vehicle_Marker=L.marker([lat,lng]).addTo(map)
//        vehicle_Marker.bindTooltip("")
         vehicle_Marker.bindPopup(`${d_id}`)

    }

    var onLeafletLoad = function (callback) {
        if (map) {
            callback();
        } else {
            leafletCallback = callback;
        }
    };

    var mapRemove=function(){
    if(map){
    map.remove()
    map=null
    }
    }

    return {
        initializeCommonLeafletMap: initializeCommonLeafletMap,
        pointMarker: pointMarker,
        onLeafletLoad: onLeafletLoad,
        mapRemove:mapRemove,
        pointVehicles:pointVehicles,
    };
});
