odoo.define('vehicle_tracking.leaflet_initialization_vehicle_track', function (require) {
    'use strict';
var map = null;
var marker = [];
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
                getGeolocation();
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


    var pointVehicles= function (lat,lng,plate_no){
        var vehicle_Marker=L.marker([lat,lng] ,{
                icon:L.icon({
                    iconUrl:'vehicle_tracking/static/description/car.png',
            iconSize: [25, 25],
            iconAnchor: [12, 24],
            popupAnchor: [0, 11]
                })
        }
        ).addTo(map)
        marker.push(vehicle_Marker)

//        vehicle_Marker.bindTooltip("")
         vehicle_Marker.bindPopup(`<div class='content_in_popup'>${plate_no}</div>`,{
          closeButton: false,
          className:'custom_popup'
         })

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
    map = null;
    marker = [];
    leafletCallback = null;
    }
    }


   var getGeolocation=function(){
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
              function (position) {
                  var currentLocation = L.latLng(position.coords.latitude, position.coords.longitude);
                   var mar= L.marker([currentLocation.lat,currentLocation.lng]).addTo(map);
                    mar.bindTooltip(`This is your current Location`)
                    map.setView(currentLocation, 14);
                    console.log("view settled at current position")
                },
                function (error) {
                    console.error('Error getting current location:', error.message);
                }
//                console.log(setLocation)
            );
        } else {
            console.error('Geolocation is not supported by this browser.');
        }

    }
    var setView_ofVehicle=function(lat,lng){
     var mark=map.setView([lat,lng], 17);
        }

    var clearAllMarker=function(){
     marker.map((a,i)=>{
     map.removeLayer(a)
     })
     }
    return {
        initializeCommonLeafletMap: initializeCommonLeafletMap,
        onLeafletLoad: onLeafletLoad,
        pointVehicles:pointVehicles,
        getGeolocation:getGeolocation,
        setView_ofVehicle:setView_ofVehicle,
        clearAllMarker:clearAllMarker,
        mapRemove:mapRemove
    };
});
