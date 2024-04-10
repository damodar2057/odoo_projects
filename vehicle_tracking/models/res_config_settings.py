# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    renewal_alert_period = fields.Integer(string='Alert Renewal', default=30, config_parameter='vehicle_tracking.renewal_alert_period')
    petrol_price=fields.Float(string='Petrol Price',default=10,config_parameter='vehicle_tracking.petrol_price')
    diesel_price=fields.Float(string='Diesel Price',config_parameter='vehicle_tracking.diesel_price')
    gasoline_price=fields.Float(string='Gasoline Price',config_parameter='vehicle_tracking.gasoline_price')

