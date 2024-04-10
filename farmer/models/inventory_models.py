from odoo import models,fields,_,api
import nepali_datetime 

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _description = 'Stock Warehouse'

    allow_external_stocks = fields.Boolean(string=_("Allow External Stocks"),default=False)
    stock_warehouse_type=fields.Selection([
        ('producer','producer'),
        ('storage','storage'),
        ('other','other'),
    ])

    # Address Information
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))

    @api.model
    def create(self, vals):
        return super(StockWarehouse, self).create(vals)