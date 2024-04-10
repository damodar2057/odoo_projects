odoo.define('vehicle_tracking.MapView', function(require) {
  'use strict';

  var BasicView = require('web.BasicView');
  var core = require('web.core');
  var MapRenderer =  require('vehicle_tracking.MapRenderer');
  var _lt = core._lt;

  var MapView = BasicView.extend({
    accesskey: 'm',
    displayname: _lt('Map'),
    icon: 'fa-map-0',
    config: _.extend({}, BasicView.prototype.config, {
            Renderer: MapRenderer,
    }),
    viewType: 'leaflet_map',

    init: function (viewInfo, params) {
        this._super.apply(this, arguments);

        var mode = this.arch.attrs.editable && !params.readonly ? "edit" : "readonly";

        this.controllerParams.mode = mode;
        this.rendererParams.arch = this.arch

        this.loadParams.limit = this.loadParams.limit || 80;
        this.loadParams.type = 'list';
    },
  });
  return MapView;

});