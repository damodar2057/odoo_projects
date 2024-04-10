import logging
import json
from odoo import http
from odoo.http import request
import xmlrpc.client
import jwt
import datetime

_secret = "my_secret_key"
_url, _db = "http://localhost:8069", 'mark_db'
_common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(_url))


class EcomClientController(http.Controller):
    _login = '/login'
    _register = '/register'
    master_url =  {
        '_sale_order' :'/order',
        '_specific_product' :'/product/<int:id>',
        "_product": '/product',
        '_product_category_name':'/product/<string:category_name>',
        '_product_category' :'/product/category',
        '_product_category_product' : '/product/category/<int:id>',
        '_invoice' :'/invoice',
        '_single_invoice': '/invoice/<int:invoice_id>',
        '_specific_sale_order' :'/order/<int:id>',
    }

    print(master_url['_sale_order'])

    _sale_order = '/order'
    _specific_product = '/product/<int:id>'
    _product = '/product'
    _product_category_name = '/product/<string:category_name>'
    _product_category = '/product/category'
    _product_category_product = '/product/category/<int:id>'
    _invoice = '/invoice'
    _single_invoice = '/invoice/<int:invoice_id>'
    _specific_sale_order = '/order/<int:id>'

    def get_partner(self, user_id):
        print(user_id)
        return http.request.env["res.users"].sudo().search([('id', '=', user_id)]).partner_id

    def convert_model_to_json(self, model):
        data_arr = []

        for rec in model:
            data = {}
            for field in rec._fields:
                data_type = type(rec[field])
                if data_type in [bool, str, int, float]:
                    data[field] = rec[field]
                else:
                    try:
                        data[field] = rec[field].id
                    except Exception:
                        continue

            data_arr.append(data)

        json_string = json.dumps(data_arr)
        return json_string

    @http.route(
        _login, type='http', auth='public', methods=['POST'], csrf=False, save_session=True
    )
    def login(self, **data):
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return json.dumps({"status": 400, "message": "Sorry, username and password must be present"})

        uid = _common.authenticate(_db, username, password, {})

        if not uid:
            return json.dumps({"status": 401, "message": "Sorry, wrong username or password"})

        # Get the current date and time
        now = datetime.datetime.utcnow()

        # Add one day to the current date and time
        expiry_date = now + datetime.timedelta(days=1)

        payload = {
            "uid": uid,
            "exp": expiry_date.timestamp()
        }

        token = jwt.encode(payload, _secret, algorithm='HS256')
        return json.dumps({"status": 200, "token": token})

    @http.route(
        _register, type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def register(self, **data):
        username = data.get('username')
        login = data.get('login')
        password = data.get('password')

        if not username or not password:
            return json.dumps({"status": 400, "message": "Sorry, username and password must be present"})

        if not login:
            return json.dumps({"status": 400, "message": "Sorry, username and password must be present"})

        user = http.request.env.user.create({
            'name': username,
            'login': login,
            'password': password,
        })
        return json.dumps({'status': 200, 'user_id': user.id})

    @http.route(
        _sale_order, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_orders(self, **data):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})

        user_id = payload['uid']
        partner = self.get_partner(user_id)

        return self.convert_model_to_json(
            http.request.env['sale.order'].sudo().search([('partner_id', '=', partner.id)]))

    @http.route(
        _sale_order, type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def create_order(self, **data):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        print(authorization_header, payload)

    @http.route(
        _specific_sale_order, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_order(self, id):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        print(authorization_header, payload)

    @http.route(
        _specific_sale_order, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def unlink_order(self, id):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        (print(authorization_header, payload)    )


    # for all products
    @http.route(
        _product, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_products(self, **kw):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        records = http.request.env['product.template'].sudo().search([])
        return self.convert_model_to_json(records)


    # for all products
    @http.route(
        '/product/tag', type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_products(self, **kw):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        records = http.request.env['product.template'].sudo().search([])
        print(records.product_tag_ids.id)

    #
    # # for product/tag
    # @http.route(
    #     '/tags/<int:id>/<int:tag_id>', type='http', auth='public', methods=['GET'], csrf=False, save_session=False,
    #
    # )
    # def get_product_with_tag(self,**kw):
    #     authorization_header = request.httprequest.headers.get('Authorization')
    #
    #     if not authorization_header:
    #         return json.dumps({"status": "401", "message": "You must have token to continue"})
    #
    #     try:
    #         payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
    #     except Exception as err:
    #         return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
    #
    #     product_id = int(kw.get('id',0))
    #     tag_id = int(kw.get('tag_id',0))
    #     products = http.request.env['product.product'].search([])
    #     if product_id:
    #         products = products.filtered(lambda p: p.id == product_id)
    #     if tag_id:
    #         products = products.filtered(lambda p: tag_id in p.product_tag_ids.id)
    #         # print(products)
    #
    #     if products:
    #         product = products[0]
    #         tag = request.env['product.tag'].browse(tag_id)
    #
    #         return request.json.dumps({
    #             'product_tag': tag.name
    #         })
    #     else:
    #         return request.json.dumps({
    #             'error': 'Product not found'
    #         })
    #     return request.json.dumps({
    #         'products': products.mapped('name')
    #     })



    @http.route(
        _specific_product, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    # for single product
    def get_product(self, **kw):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        # print(authorization_header, payload)
        product_category_id = kw.get('id')
        records = http.request.env['product.template'].sudo().search([('id','=',product_category_id)])

        return self.convert_model_to_json(records)

    # for single product with category name

    @http.route(
        _product_category_name , type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_product(self, **kw):
        authorization_header = request.httprequest.headers.get('Authorization')

        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        print(authorization_header, payload)
        product_category_name = kw.get('category_name')
        records = http.request.env['product.template'].sudo().search([('name','=',product_category_name)])
        return self.convert_model_to_json(records)

        # for product category
    @http.route(
        _product_category, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_product_categories(self, **kw):
        authorization_header = request.httprequest.headers.get('Authorization')
        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        print(authorization_header, payload)
        records = http.request.env['product.product'].sudo().search([])
        return self.convert_model_to_json(records)

        # Single product for  product category
    @http.route(
        _product_category_product, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_product_category(self, **kw):

        authorization_header = request.httprequest.headers.get('Authorization')


        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        product_category_id = kw.get('id')
        print(product_category_id)
        records =  http.request.env['product.product'].sudo().search([('id','=',product_category_id)])
        return self.convert_model_to_json(records)


        # For Invoice
    @http.route(
        _invoice, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_invoices(self, **kw):

        authorization_header = request.httprequest.headers.get('Authorization')


        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])
        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        print(authorization_header, payload)
        records = http.request.env['account.move'].sudo().search([])
        return self.convert_model_to_json(records)



        # For Single Invoice
    @http.route(
        _single_invoice, type='http', auth='public', methods=['GET'], csrf=False, save_session=False
    )
    def get_invoice(self, **kw):

        authorization_header = request.httprequest.headers.get('Authorization')


        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])


        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        print(authorization_header, payload)
        single_invoice_id = kw.get('invoice_id')
        return self.convert_model_to_json(
            http.request.env['account.move'].sudo().search([('id', '=', single_invoice_id)]))



        # Post payment transcation
    @http.route(
        '/create-payment', type='http', auth='public', methods=['POST'], csrf=False, save_session=False )
    def get_invoice(self, **kw):
        authorization_header = request.httprequest.headers.get('Authorization')


        if not authorization_header:
            return json.dumps({"status": "401", "message": "You must have token to continue"})

        try:
            payload = jwt.decode(authorization_header.encode(), _secret, algorithms=['HS256'])


        except Exception as err:
            return json.dumps({"status": "401", "message": "Wrong authentication token provided"})
        # print(authorization_header, payload)
        amount = float(kw.get('amount',0.0))
        reference = kw.get('reference')
        # self.ensure_one()
        provider_id = kw.get('provider_id')
        partner_id = kw.get('partner_id')
        currency_id = kw.get('currency_id')
        partner = request.env['res.partner'].sudo().search([('id','=',partner_id)])
        partner = partner['id']
        provider = request.env['payment.provider'].sudo().search([('id','=',provider_id)])
        currency = request.env['res.currency'].sudo().search([('id','=',currency_id)])
        currency = currency['id']
        provider = provider.id
        if not partner:
            return json.dumps({"status": "400", "message": "Partner not found"})
        return self.convert_model_to_json(

            http.request.env['payment.transaction'].sudo().create({
                'amount':amount,
                'reference':reference,
                'provider_id':provider,
                'partner_id':partner,
                'currency_id':currency,
            }
            ))

