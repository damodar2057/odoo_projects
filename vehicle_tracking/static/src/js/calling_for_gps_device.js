odoo.define("vehicle_tracking.calling_for_gps_device", function (require) {
  "use strict";

  var rpc = require("web.rpc");
  const updateMap = () => {
    console.log("called");
    rpc
      .query({
        model: "vehicle.location",
        method: "get_device_location",
        args: ["vehicle.location"],
      })
      .then(function (result) {
        console.log("python method called");
      });
    //                             Create a new layer and render fresh records
    //                this.leaflet_layer_group = L.layerGroup().addTo(this.leaflet_map);
    //                _.each(this.state.data, function (record) {
    //                    self._renderRecord(record);
    //                });
  };

  setInterval(updateMap, 500000);
});
