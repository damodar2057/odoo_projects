from odoo import models,api,fields


class StocKWarehouseInherit(models.Model):
    _inherit = 'stock.warehouse'

    latitude = fields.Float("Latitude",required=True)
    longitude = fields.Float("Longitude",required=True)

   # Warehouse coordinates should be added to the map and also the shipping address and also other routing is also important
    # picking and delivery address and many more
    @api.model
    def get_warehouse_data(self):
        print("Hello")
        # Retrieves warehouse records with coordinates
        warehouse_location = self.search([])
        print(warehouse_location)

        # creates a list of dictionaries containing warehouse data
        warehouse_data = []
        for warehouse in warehouse_location:
            warehouse_data.append({
                'id':warehouse.id,
                'name': warehouse.name,
                'latitude': warehouse.latitude,
                'longitude': warehouse.longitude,


            })
        print(warehouse_data)
        return warehouse_data




