odoo.define('vehicle_tracking.MapRenderer', function (require) {
    'use strict';

    var AbstractRenderer = require('web.AbstractRenderer');
    var session = require('web.session');
    var field_utils = require('web.field_utils');

    var MapRenderer = AbstractRenderer.extend({
        tagName: 'div',
        className: 'o_leaflet_main_container',

        init: function (parent, state, params) {


            this._super.apply(this, arguments);

            this.leaflet_tile_url = session['leaflet.tile_url'];
            this.leaflet_copyright = session['leaflet.copyright'];
            this.default_zoom = params.arch.attrs.default_zoom || 7;
            this.max_zoom = params.arch.attrs.max_zoom || 19;
            this.zoom_snap = params.arch.attrs.zoom_snap | 1;
            this.field_latitude = params.arch.attrs.latitude;
            this.field_longitude = params.arch.attrs.longitude;
            this.field_title = params.arch.attrs.field_title;
            this.field_time = params.arch.attrs.field_time;
            this.field_address = params.arch.attrs.address;
            this.field_marker_icon_image = params.arch.attrs.field_marker_icon_image;
            this.marker_icon_size_x = params.arch.attrs.marker_icon_size_x || 22;
            this.marker_icon_size_y = params.arch.attrs.marker_icon_size_y || 22;
            this.marker_popup_anchor_x = params.arch.attrs.marker_popup_anchor_x || 0;
            this.marker_popup_anchor_y = params.arch.attrs.marker_popup_anchor_y || -32;
        },

        start: function () {
            var self = this;
            var self_super = this._super;
            var componentInstance = null;


           // Initial execution
           function reloadComponent() {
                if (componentInstance) {

                }
                var savedState = self.currentState;
                self._initDefaultPosition().then(function () {
                    self._initMap();
//                    self._render()
                }).then(function () {
                            self.currentState = savedState;
                    componentInstance = self_super.apply(self, arguments);
                    return componentInstance;
                })
           }
           //Initial execution
           reloadComponent()

        },

        _render: function () {
            var self = this;

//            // First remove previous layer that contains
//
//                    // Clear existing markers and polylines before adding new ones
//        this.leaflet_map.eachLayer(layer => {
//            if (layer instanceof L.Marker || layer instanceof L.Polyline) {
//                this.leaflet_map.removeLayer(layer);
//            }
//        });


             const updateMap = () => {
                this._rpc({
                    model: "vehicle.location",
                    method: 'get_device_location',
                    args: [this.state.model],
                }).then(function (result) {
                    self.default_lat_lng = L.latLng(result.lat, result.lng);
                   self.field_time = result.time
                })
                            // Create a new layer and render fresh records
                this.leaflet_layer_group = L.layerGroup().addTo(this.leaflet_map);
                _.each(this.state.data, function (record) {
                    self._renderRecord(record);
                });

             }

            this._loadWarehouse();
            setInterval(updateMap, 20000);




        },
        _loadWarehouse: function () {
            var self = this;
            console.log("hello")

            // Fetch warehouse data from the server
            this._rpc({
                model: "stock.warehouse",
                method: 'get_warehouse_data',
            }).then(function (warehouses) {
                // Create a new layer and render warehouse locations
                var warehouseLayer = L.layerGroup().addTo(self.leaflet_map);

                warehouses.forEach(function (warehouse) {
                    self._renderWarehouse(warehouse, warehouseLayer);
                });
            });
        },
        _renderWarehouse: function (warehouse, warehouseLayer) {
            var self = this;
            var latlng = L.latLng(warehouse.latitude, warehouse.longitude);
            var warehouseIcon = L.icon({
                iconUrl: session.url('/vehicle_tracking/static/description/warehouse_icon.png'),
                iconSize: [22,22]
            })

            // Display only warehouses that have a valid position
            if (latlng.lat != 0 && latlng.lng != 0) {
                // Create marker for warehouse
//                var markerOptions = self._prepareWarehouseMarkerOptions(warehouse);
                var warehouseMarker = L.marker(latlng,{icon: warehouseIcon}).addTo(warehouseLayer);

                var popupContent = `
                    <strong>Warehouse Name:</strong> ${warehouse.name}<br>
                    <strong>Latitude:</strong> ${warehouse.latitude}<br>
                    <strong>Longitude:</strong> ${warehouse.longitude}<br>
                `;

                warehouseMarker.bindPopup(popupContent).openPopup();
            }
        },


        _renderRecord: function(record) {
            var self = this;
            // Set latitude and longitude for Nepal
            var nepalLat = 28.3949; // Replace with the actual latitude for Nepal
            var nepalLng = 84.1240; // Replace with the actual longitude for Nepal



            // Use the provided values or fallback to the record's data
            var lat = record.data.latitude || nepalLat;
            var lng = record.data.longitude || nepalLng;


            var latlng = L.latLng(lat, lng);

            // Display only records that have a valid position
            if (latlng.lat != 0 && latlng.lng != 0) {
                // create marker
                var markerOptions = this._prepareMarkerOptions(record);
                var marker = L.marker(latlng).addTo(this.leaflet_layer_group);
                var popupContent = `
                <strong>Latitude:</strong> ${record.data.latitude}<br>
                <strong>Longitude:</strong> ${record.data.longitude}<br>
                <strong>Time:</strong> ${self.field_time}<br>
                <strong>Address:</strong> ${record.data.address}<br>
            `;

            marker.bindPopup(popupContent).openPopup();
                var popup = L.popup().setContent(this._preparePopUpData(record));

//                marker.bindPopup(popup).on("popupopen", () => {
//                    $(".o_map_selector").parent().parent().click({model_name: record.model, res_id: record.data["id"], current_object: self}, self._onClickLeafletPopup);
//                });

            }
        },

        _onClickLeafletPopup: function (ev) {
            ev.preventDefault();
            ev.data.current_object.trigger_up('switch_view', {
                view_type: 'form',
                res_id: ev.data.res_id,
                model: ev.data.model_name,
            });
        },

        _prepareMarkerIcon: function(record) {
            var myIcon = L.icon({
                iconUrl: session.url('/web/image', {
                    model: record.model,
                    id: JSON.stringify(record.data.id),
                    field: this.field_marker_icon_image,
                    // unique forces a reload of the image when the record has been updated
                   unique: field_utils.format.datetime(record.data.__last_update).replace(/[^0-9]/g, ''),
                }),
                className: "leaflet_marker_icon",
                iconSize: [this.marker_icon_size_x, this.marker_icon_size_y],
                popupAnchor: [this.marker_popup_anchor_x, this.marker_popup_anchor_y],
            });
            return myIcon;

        },

        _prepareMarkerOptions: function (record) {
            var icon = this._prepareMarkerIcon(record);
            var result = {
                address: record.data.address,
                alt: record.data[this.field_title],
                riseOnHover: true,
            }
            if (icon) {
                result.icon = icon;
            }
            return result;
        },

        _preparePopUpData: function (record) {
            return (
                "<div class='o_map_selector' res_id='" + record.data["id"] + "'>"
                + "<b>" + record.data.gps_time + "</b><br/>"
                + " - " + record.data.address
                + "</div>"
            );
        },

        _initDefaultPosition: function () {
            var self = this;
            return new Promise(function(resolve, reject) {
                self.default_lat_lng = L.latLng(28.3949, 84.1240);
                resolve(self.default_lat_lng);
            });
        },

        _initMap: function () {
            var $mainDiv = $("<div id='div_map' class='o_leaflet_map_container'/>");
            this.leaflet_container = $mainDiv[0];
            this.leaflet_map = L.map(this.leaflet_container, {
                zoomSnap: this.zoom_snap,
            }).setView(this.default_lat_lng, this.default_zoom);
            this.leaflet_tiles = L.tileLayer(this.leaflet_tile_url, {
                maxZoom: this.max_zoom,
                attribution: this.leaflet_copyright,
            }).addTo(this.leaflet_map);
            L.marker(this.default_lat_lng).addTo(this.leaflet_map)
            this.$el.append($mainDiv);
        },


    });

    return MapRenderer;

});