from odoo import http, models, fields

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal



class PriceNegotiationController(http.Controller):

    @http.route('/price/negotiation/', type='http',website=True, auth='public',csrf=False)
    def price_negotiation_form(self, **kw):
        product_name = kw.get('product_name')
        # print(product_name)
        product_price = kw.get('product_price')
        min_quantity = kw.get('min_quantity')
        product_id = kw.get('product_id')
        current_user = request.env.user
        user_name = current_user.name
        # print(user_name)
        user_email = current_user.email
        user_phone = current_user.phone
        return request.render('price_negotiation.price_negotiation_request_template',{
            'default_product_name': product_name,
            'default_product_price': product_price,
            'default_min_quantity': min_quantity,
            'default_customer': user_name,
            'default_product_id':product_id,
            'default_user_email': user_email,
            'default_user_phone': user_phone,
        })
    # @http.route('/price/negotiation', type='http',methods=['POST'], website=True, auth='public',csrf=False)
    # def price_negotiation_form(self, **kw):
    #     payload = request.httprequest.data.decode('utf-8')
    #     product_name = json.loads(payload).get('product_name')
    #     product_price = json.loads(payload).get('product_price')
    #     min_quantity = json.loads(payload).get('min_quantity')
    #     product_id = json.loads(payload).get('product_id')
    #     current_user = request.env.user
    #     user_name = current_user.name
    #     user_email = current_user.email
    #     user_phone = current_user.phone
    #     return request.render('price_negotiation.price_negotiation_request_template',{
    #         'default_product_name': product_name,
    #         'default_product_price': product_price,
    #         'default_min_quantity': min_quantity,
    #         'default_customer': user_name,
    #         'default_product_id':product_id,
    #         'default_user_email': user_email,
    #         'default_user_phone': user_phone,
    #     })


    @http.route('/price/negotiation/submit', type='http',website=True, auth='public',csrf=False)
    def price_negotiation_submit(self, **kw):
        print("Hello")
        customer = kw.get('inputCustomer4')
        email =  kw.get('inputEmail4'),
        print(email)

        print(customer)
        negotiation = http.request.env['price.negotiation'].create({
            'customer': kw.get('inputCustomer4'),
            'email': kw.get('inputEmail4'),
            'product':  kw.get('inputProductID'),
            'product_name': kw.get('inputProduct'),
            'quantity': kw.get('inputQuantity'),
            'phone': kw.get('inputPhone'),
            'actual_price': kw.get('inputActualPrice'),
            'expected_price_per_unit': kw.get('inputExpectedPrice'),
            'description': kw.get('inputDescription'),
            'customer_status': kw.get('inputStatus'),

        })
        return request.render("price_negotiation.negotiation_request_success_template")
        # return negotiation


# class CustomerPortalExtendedController(CustomerPortal):
#
#     def _prepare_home_portal_values(self,counters):
#         response = super(CustomerPortalExtendedController,self)._prepare_home_portal_values(counters)
#         response['negotiation_count'] = request.env['price.negotiation'].search_count([])
#         return response
#
#     @http.route(['/my/negotiations'],type='http', website=True)
#     def negotiation_listview(self,**kw):
#         return None
#

