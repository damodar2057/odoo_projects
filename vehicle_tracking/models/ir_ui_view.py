from odoo import fields, models, api,SUPERUSER_ID


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('leaflet_map', 'Leaflet Map')])


class IrActionsActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(
        selection_add=[('leaflet_map', 'Leaflet Map')],
        ondelete={'leaflet_map': 'cascade'}  # Define the ondelete policy here
    )


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(Http, self).session_info()
        config = self.env['ir.config_parameter'].sudo()
        result.update({
            "leaflet.tile_url": config.get_param('leaflet.tile_url', default=''),
            "leaflet.copyright": config.get_param('leaflet.copyright', default=''),
        })
        return result

class ResUsers(models.Model):
    _inherit = 'res.users'

    field_latitude = fields.Char()
    field_longitude = fields.Char()
    field_title = fields.Char()
    field_address = fields.Char()
    is_driver = fields.Boolean("Is Driver")

    @api.model
    def get_default_leaflet_position(self, model_name):
        print("Hello")
        current_partner = self.env.user.company_id.partner_id
        print(current_partner)
        return {
            "lat": current_partner.partner_latitude,
            "lng": current_partner.partner_longitude,
        }

    @api.model
    def create(self, vals_list):
        user = super(ResUsers, self).create(vals_list)

        # Check if the user is a driver
        if user.is_driver:
            # Get the ID of the "Registered Vehicle Driver" group
            driver_group_id = self.env.ref('vehicle_tracking.group_driver_access')

            # Add the user to the "Registered Vehicle Driver" group
            user.write({'groups_id': [(4, driver_group_id.id)]})

        return user

class ResPartner(models.Model):
    _inherit = 'res.partner'

    latitude = fields.Float(string="Latitude",digits=(10,7))
    longitude = fields.Float(string="Longitude",digits=(10,7))

    @api.model
    def get_default_leaflet_position(self, model_name):
        print("Hello")
        current_partner = self.env.user.company_id.partner_id
        print(current_partner)
        return {
            "lat": current_partner.partner_latitude,
            "lng": current_partner.partner_longitude,
        }

#
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#
#     assigned_vehicle_id = fields.Char()
#     warehouse_ref = self.env.ref['fleet.vehicle']
#




class StockPicking(models.Model):
    _inherit = 'stock.picking'


    # assigned_vehicle_id = fields.Char()
    assigned_vehicle = fields.Many2one('driver.current.state.location',"Assigned Vehicle",
                                        domain="[('status','=',False)]",
                                       ondelete='cascade'
                                        )



