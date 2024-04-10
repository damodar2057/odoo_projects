odoo.define('vehicle_tracking.Test',['web.Widget'],function (require) {
   "use strict";
   const Widget = require("web.Widget");
   console.log(Widget)

   console.log("This is from outside the extension of the widget")




   var UserMapView = Widget.extend({
        template: 'vehicle_tracking.track_order_template',

        init: function(parent){
               console.log("Hello")
            this._super.apply(this,arguments);
            this.vehicleCoordinates = [0,0];
            console.log(this.vehicleCoordinates)
            this.warehouseCoordinates = [0,0];
            this.shippingCoordinates = [0,0];
            this.updateInitialCoordinates();
            this.updateVehicleCurrentCoordinates();
            this.intervalId = setInterval(this.updateVehicleCurrentCoordinates.bind(this),20000);
        },

        updateInitialCoordinates: function () {
            var self = this;

            // Make an Ajax request to fetch the initial coordinates from the controller
            this._rpc({
                route: '/get_initial_coordinates',
                }).then(function (response) {
                    self.vehicleCoordinates = [response.assigned_vehicle_current_coordinates.latitude, response.assigned_vehicle_current_coordinates.longitude];
                    self.warehouseCoordinates = [response.source_location.latitude, response.source_location.longitude];
                    self.shippingCoordinates = [response.destination_location.latitude, response.destination_location.longitude];
                    self.render_map();
                });
        },

        updateVehicleCoordinates: function () {
            var self = this;

            // Make an Ajax request to fetch the latest vehicle coordinates from the controller
            this._rpc({
                route: '/update_assigned_vehicle_location',
                }).then(function (response) {
                    if (response.status === 'success' && response.data.length > 0) {
                        var latestCoordinates = response.data[0];
                        self.vehicleCoordinates = [latestCoordinates.latitude, latestCoordinates.longitude];
                        self.render_map();
                    }
                });
        },



        start: function() {
            this.render_map();
            return this._super.apply(this,arguments);
        },

        render_map: function() {
            var map = L.map('map').setView(this.vehicleCoordinates,id);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            var vehicleMarker = L.marker(this.vehicleCoordinates).addTo(map);
            var warehouseMarker = L.marker(this.warehouseCoordinates).addTo(map);
            var shippingMarker = L.marker(this.shippingCoordinates).addTo(map);

            // Draw a polyline from warehouse to shipping
            var polyline = L.polyline([this.warehouseCoordinates, this.VehicleCoordinates],{color: 'blue'}).addTo(map);

            map.fitBounds([this.vehicleCoordinates, this.warehouseCoordinates, this.shippingCoordinates]);
        },

        destroy: function () {
            clearInterval(this.intervalId);
            this._super.apply(this, arguments);
        },
   });

    return UserMapView;


});