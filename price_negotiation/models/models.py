# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PriceNegotiation(models.Model):
    _inherit = 'product.template'

    is_negotiation_allowed = fields.Boolean("Allow Negotiation")
    min_quantity = fields.Integer("Minimum Negotiable Quantity")

    # if not is_negotiation_allowed:






