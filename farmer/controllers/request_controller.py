from odoo import http
from odoo.http import request
import json

class ServiceRequest(http.Controller):

    @http.route('/request/service_request', type='http', website=True, auth="public")
    def submit_form(self, **kw):
            return request.render('farmer.request_service_request_template', {})

    @http.route('/create/request/service_request', type='http', website=True, auth="public", Methods=['POST'])
    def create_form(self, **kw):
        if len(kw)==0:
            return request.render('farmer.request_service_request_template', {})
        try:
            uid = request.uid
            producer_id = request.env['farm.producer'].search_read([('user_id','=',uid)],['id'])[0]['id']
            values = {
                'service_name': int(kw['service_name']),
                'service_recipient': producer_id,
            }
            form_id = request.env['services.request'].sudo().create(values)
            print(form_id)
            return request.render('farmer.request_request_success_template', {'request_code':form_id.ref})
        except:
            return request.render('farmer.request_service_request_template', {'message':'Invalid Value Sent!!! Please send again...'})

class EquipmentRequest(http.Controller):

    @http.route('/request/equipment_request', type='http', website=True, auth="public")
    def submit_form(self, **kw):
            return request.render('farmer.request_equipment_request_template', {})

    @http.route('/create/request/equipment_request', type='http', website=True, auth="public", Methods=['POST'])
    def create_form(self, **kw):
        if len(kw)==0:
            return request.render('farmer.request_equipment_request_template', {})
        try:
            uid = request.uid
            producer_id = request.env['farm.producer'].search_read([('user_id','=',uid)],['id'])[0]['id']
            values = {
                'equipment_type': int(kw['equipment_type']),
                'equipment_quantity': kw['equipment_quantity'],
                'equipment_recipient': producer_id,
            }
            form_id = request.env['equipment.request'].sudo().create(values)
            return request.render('farmer.request_request_success_template', {'request_code':form_id.ref})
        except:
            return request.render('farmer.request_equipment_request_template', {'message':'Invalid Value Sent!!! Please send again...'})

class SeedlingRequest(http.Controller):

    @http.route('/request/seedling_request', type='http', website=True, auth="public")
    def submit_form(self, **kw):
            return request.render('farmer.request_seedling_request_template', {})

    @http.route('/create/request/seedling_request', type='http', website=True, auth="public", Methods=['POST'])
    def create_form(self, **kw):
        if len(kw)==0:
            return request.render('farmer.request_seedling_request_template', {})
        try:
            uid = request.uid
            producer_id = request.env['farm.producer'].search_read([('user_id','=',uid)],['id'])[0]['id']
            # print(kw["seedling_list"])
            # print(kw['seedling_list'][0])
            # print(kw['seedling_list'][1:].split(', ')+[kw['seedling_list'][0]])
            seedling_list = [int(i) for i in kw["seedling_list"].split(',')]

            values = {
                'seedling_list': seedling_list,
                'seedling_quantity': kw['seedling_quantity'],
                'seedling_recipient': producer_id,
            }
            form_id = request.env['seedling.request'].sudo().create(values)
            return request.render('farmer.request_request_success_template', {'request_code':form_id.ref})
        except:
            return request.render('farmer.request_seedling_request_template', {'message':'Invalid Value Sent!!! Please send again...'})

class ExpertRequest(http.Controller):

    @http.route('/request/expert_request', type='http', website=True, auth="public")
    def submit_form(self, **kw):
            return request.render('farmer.request_expert_request_template', {})

    @http.route('/create/request/expert_request', type='http', website=True, auth="public", Methods=['POST'])
    def create_form(self, **kw):
        if len(kw)==0:
            return request.render('farmer.request_expert_request_template', {})

        try:
            uid = request.uid
            producer_id = request.env['farm.producer'].search_read([('user_id','=',uid)],['id'])[0]['id']
            values = {
                'expert_id': int(kw['expert_id']),
                'expert_recipient': producer_id,
            }
            form_id = request.env['expert.request'].sudo().create(values)
            return request.render('farmer.request_request_success_template', {'request_code':form_id.ref})
        except:
            return request.render('farmer.request_expert_request_template', {'message':'Invalid Value Sent!!! Please send again...'})



