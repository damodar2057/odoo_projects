from odoo import http
from odoo.http import request

class PartnerController(http.Controller):

    @http.route('/get_partner', type='http', auth='public', website=True)
    def get_partner(self, partner_id=2):
        if partner_id:
            partner = request.env['res.partner'].browse(int(partner_id))
            if partner:
                # You can access the partner's attributes here
                partner_name = partner.name
                partner_email = partner.email
                partner_phone = partner.phone

                # You can return the partner's information as JSON or HTML, depending on your needs
                response_data = {
                    'name': partner_name,
                    'email': partner_email,
                    'phone': partner_phone,
                }

                return (response_data)