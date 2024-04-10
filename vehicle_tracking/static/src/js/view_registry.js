odoo.define('vehicle_tracking.view_registry', function(require){
    "use strict";

    var MapView = require('vehicle_tracking.MapView');
    var view_registry = require('web.view_registry');

    view_registry.add('leaflet_map', MapView)
})