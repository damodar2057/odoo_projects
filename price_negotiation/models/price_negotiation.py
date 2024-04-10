# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import random
import string
from datetime import datetime, timedelta



class PriceNegotiation(models.Model):
    _name = 'price.negotiation'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin',]

    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Negotiation ID'), )
    customer = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    company = fields.Char()
    description = fields.Text()
    request_datetime = fields.Datetime(default=lambda self: fields.Datetime.now())
    product = fields.Char()
    quantity = fields.Char()
    customer_price_list = fields.Char()
    actual_price = fields.Float()

    def _get_default_counter_offer_price(self):
        print(self.actual_price)
        # Get the value of actual_price from the record or set a default value
        return self.actual_price or 0.0  # A

    counter_offer_price_per_unit = fields.Float(default=0.0,tracking=True)
    expected_price_per_unit = fields.Float(tracking=True)
    negotiation_promo_code = fields.Char(string='Negotiation Promo Code')
    customer_status = fields.Char(tracking=True)
    product_name = fields.Char()
    final_negotiated_price = fields.Float(compute='_final_negotiated_price',default=0.0,tracking=True)
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('On Negotiation', 'On Negotiation'),
        ('Accept', 'Accept'),
        ('Reject', 'Reject'),
        ('Done', 'Done'),
    ], default='Draft', readonly=True, string="State", tracking=True)

    @api.depends('state', 'customer_status', 'expected_price_per_unit')
    def _final_negotiated_price(self):
        for record in self:
            if record.state == 'Accept' and record.customer_status == 'Locked':
                record.final_negotiated_price = record.expected_price_per_unit
            else:
                record.final_negotiated_price = 0.0  # or any default value if needed


    def _get_negotiated_price(self):
        if self.state == 'Done':
            # Return the Negotiated Price
            return self.negotiation_promo_code
        else:
            # return the actual price
            return self.actual_price

    @api.depends('state')
    def _compute_negotiated_price(self):
        for record in self:
            record.negotiated_price = record._get_negotiated_price()

    negotiated_price = fields.Char(compute='_compute_negotiated_price', string='Negotiated Price')

    @staticmethod
    def generate_negotiation_token(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=14))

    negotiation_token = fields.Char(default=generate_negotiation_token)

    @staticmethod
    def generate_promo_code(self):
        # Generate a random promo code
        promo_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # # Create a record for the promo code
        # promo_code_obj = self.env['sale.coupon.program']
        # promo_code_record = promo_code_obj.create({
        #     'name': 'Promo for Negotiation',  # Name of the promo code
        #     'promo_code_usage': 'code_needed',  # Method of using the promo code
        #     'promo_code': promo_code,  # Assign the generated promo code
        #     'active': True,  # Set the promo code as active
        #     # Add more fields as per your requirements
        # })

        return promo_code  # Return the generated promo code


    def accept_request(self):
        self.state = 'Accept'
        default_start_date = datetime.now()
        default_end_date = default_start_date + timedelta(days=7)

        # # Call the method to generate the promo code
        # generated_promo_code = self.generate_promo_code()
        # generated_token = self.generate_negotiation_token()
        # print(generated_promo_code)
        # print(generated_token)


        # create a record in the product.pricelist model
        product_template = self.env['product.template'].search([('id', '=', int(self.product))])
        product_name = product_template.name
        print(product_name)
        self.negotiation_promo_code = self.generate_promo_code(self)

        pricelist_obj = self.env['product.pricelist']
        pricelist_record = pricelist_obj.with_context(from_negotiation_model=True).create({
            'name': 'Negotiated Pricelist for {}'.format(self.customer),
            'code':self.negotiation_promo_code,
            # 'is_negotiation_pricelist': True,
            # 'type': 'sale',
            'item_ids':[(0,0, {

                'min_quantity':product_template.min_quantity,
                # 'applied_on': 'o_product_variant',
                # 'price': self.negotiated_price,
                'compute_price': 'fixed',
                'fixed_price': self.final_negotiated_price,
                'applied_on': '1_product',
                'product_tmpl_id': product_template.id,
                'date_start': default_start_date,
                'date_end': default_end_date,    # Setting validity end date
                # 'product_id': 47,
                # 'product_id': self.normal_delivery.product_id.id,

            })],
            'currency_id': self.env.ref('base.USD').id,

            # 'currency_id': self.env.company.currency_id.id,
        })
        # # Associate the generated promo code with the negotiation record
        # self.write({
        #     'negotiation_promo_code': pricelist_record.id,
        #
        #     # 'negotiation_token': generated_token
        #     # Assuming 'promo_code' is a field in your model to store the code
        # })
    def reject_request(self):
        self.state = 'Reject'

    def mark_as_done(self):
        # self.final_locked_price = self.negotiated_price
        self.state = 'Done'

    def mark_as_undo(self):
        self.state = 'Accept'

    def action_open_counter_offer_popup(self):
        return {
            'name': 'Enter Counter Offer Price',
            'type': 'ir.actions.act_window',
            'res_model': 'price.negotiation.counter.offer.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('price_negotiation.view_price_negotiation_counter_offer_popup').id,
            'target': 'new',
            'context': {
                'default_price_negotiation_id': self.id,
            }
        }

    def update_counter_offer_price(self, counter_offer_price):
        if counter_offer_price:
            self.write({'counter_offer_price_per_unit': counter_offer_price})
            self.state = 'On Negotiation'
        else:
            self.state = 'Draft'

    def not_allow_to_on_negotiation_state(self):
        self.state = 'Draft'

    def contact_customer(self):
        if self.state == 'Accept':
            template_ref = self.env.ref('price_negotiation.price_negotiation_email_template_accept')
            return template_ref.send_mail(self.id, force_send=True)
        elif self.state == 'Reject':
            template_ref = self.env.ref('price_negotiation.price_negotiation_email_template_reject')
            return template_ref.send_mail(self.id, force_send=True)
        elif self.state == 'On Negotiation':
            return self.action_quotation_send()

    def action_quotation_send(self):
        print("hello")
        self.ensure_one()
        lang = self.env.context.get('lang')
        template_ref = self.env.ref('price_negotiation.price_negotiation_email_template_on_negotiation')
        mail_template = template_ref
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]

        ctx = {
            'default_model': 'price.negotiation',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,

        }
        print(ctx)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("price.negotiation.request.sequence")
        # vals['saved'] = True
        record = super(PriceNegotiation, self).create(vals)
        return record

class PriceNegotiationCounterOfferWizard(models.TransientModel):
    _name = 'price.negotiation.counter.offer.wizard'
    _description = 'Counter Offer Price Wizard'

    price_negotiation_id = fields.Many2one('price.negotiation', string='Price Negotiation')
    counter_offer_price = fields.Float(string='Counter Offer Price')

    def update_counter_offer_price(self):
        self.price_negotiation_id.update_counter_offer_price(self.counter_offer_price)
        return {'type': 'ir.actions.act_window_close'}










