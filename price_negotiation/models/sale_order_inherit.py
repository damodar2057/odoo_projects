# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'sale':
            for order in self:
                print(vals['state'])
                # print(vals['pricelist_id'])

                pricelist_id = order.pricelist_id
                # print(pricelist_id)
                # pricelist_item_id = pricelist_id.item_ids
                # print(pricelist_item_id)
                print("Archive is not done")
                if pricelist_id.is_negotiation_pricelist:
                    pricelist_id.active = False
                    # validity_start_date = pricelist_item_id.date_start
                    # print(validity_start_date)
                    # pricelist_item_id.date_end = validity_start_date
                    # # print(validity_date_end)
                    order.pricelist_id = pricelist_id
                    print("Archive is done")
                    # vals['pricelist_id'] = order.pricelist_id
                    # print(pricelist_id)

        return super(SaleOrderInherit, self).write(vals)


class ProductPricelistInherit(models.Model):
    _inherit = 'product.pricelist'

    is_negotiation_pricelist = fields.Boolean()
    # is_negotiation_pricelist_used = fields.Boolean(default=False)

    @api.model
    def create(self, vals_list):
        if 'from_negotiation_model' in self.env.context:
            vals_list['is_negotiation_pricelist'] = True
        else:
            vals_list['is_negotiation_pricelist'] = False
        return super(ProductPricelistInherit,self).create(vals_list)


    # @api.model
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals['state'] == 'sale':
    #             pricelist_id = vals['pricelist_id']
    #             is_negotiation_pricelist_used = pricelist_id.is_negotiation_pricelist_used
    #             if  is_negotiation_pricelist_used == False
    #                 pricelist_id.is_negotiation_pricelist_used = True
    #                 vals['pricelist_id'] = pricelist_id
    #     return super().create(vals)
    #


        # track_promo_code_usage = fields.Integer()
        #
        # pricelist_id =
        # def check(self):
        #
        #     price_list_id = self.env.ref['product.pricelist']
        #
        # @api.model()
        # def create(self, vals_list):
        #
        #
        # if (track_promo_code_usage > 1):
        #     validity_enddate = validity_startdate


    #
    # def update_pricelist_record(self):
    #     for order in self:
    #         # Check if pricelist_id is set in the order
    #         if order.pricelist_id:
    #             # Access the pricelist record based on pricelist_id
    #             pricelist_record = order.pricelist_id
    #             # Perform operations on the pricelist record
    #             validity_start_date = pricelist_record.date_start
    #             pricelist_record.date_end = validity_start_date
    #
    #     # === CRUD METHODS ===#
