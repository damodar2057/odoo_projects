/** @odoo-module **/

import {registry} from '@web/core/registry';
const {Component,onMounted,useState}=owl;

export class LeafletPractice extends Component{
setup(){
this.state=useState({
coordinates:{lat:'',lng:''},
selects:{lat:'',lng:''}
})
onMounted(async()=>{
await this.loadLeaflet()
})
}
async loadLeaflet(){
console.log("leaflet here")
let getLocation={lat:'',lng:''};
const leafletCssLink = document.createElement('link');
    leafletCssLink.rel = 'stylesheet';
    leafletCssLink.href = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css';
    document.head.appendChild(leafletCssLink);

 const leafletScript = document.createElement('script');
        leafletScript.src = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js';
        leafletScript.async = true;
        document.head.appendChild(leafletScript);

      leafletScript.onload = () => {
            // Initialize Leaflet map
            const map = L.map('leaflet-map').setView([27.70205085666016, 85.30125712592734], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);
            if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
           (position)=> {
           let  currentLocation = L.latLng(position.coords.latitude, position.coords.longitude);
            map.setView(currentLocation, 13);
          let draggableMarker=L.marker(currentLocation,{
          draggable:true
          }).addTo(map);
          getLocation=currentLocation;
          console.log(getLocation)
            this.state.coordinates={lat:getLocation.lat,lng:getLocation.lng}

          draggableMarker.on('dragend', (event)=> {
                        const marker = event.target;
                        const position = marker.getLatLng();
                        console.log('Marker dragged to:', position.lat, position.lng);
                        this.state.selects={lat:position.lat,lng:position.lng}

                    });
          },


          function (error) {
            console.error('Error getting current location:', error.message);
          }
        );
      } else {
        console.error('Geolocation is not supported by this browser.');
      }

            $(document).ready(function () {
    $('#exampleModal').on('shown.bs.modal', function () {
        map.invalidateSize();
    });
});
            }
}
selectLocation(){
this.state.coordinates=this.state.selects;

}
}

LeafletPractice.template='leaflet.practice'
registry.category('actions').add('vehicle_tracking.leaflet.practice.action',LeafletPractice);
