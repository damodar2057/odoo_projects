from odoo import http
from odoo.http import request
import json

class ProfileView(http.Controller):

    @http.route('/request/profile_view', type='http', website=True, auth="public")
    def submit_form(self, **kw):
        uid = request.uid
        farmer_id=0
        household_id=0
        farmer_group_id=0
        if len(request.env['farm.farmer'].search_read([('user_id','=',uid)],['id'])) > 0:
            farmer_id = request.env['farm.farmer'].search_read([('user_id','=',uid)],['id'])[0]['id']
        if len(request.env['farm.household'].search_read([('user_id','=',uid)],['id'])) > 0:
            household_id = request.env['farm.household'].search_read([('user_id','=',uid)],['id'])[0]['id']
        if len(request.env['farmer.group'].search_read([('user_id','=',uid)],['id'])) > 0:
            farmer_group_id = request.env['farmer.group'].search_read([('user_id','=',uid)],['id'])[0]['id']
        if farmer_id:
            try:
                action = request.env.ref('farmer.action_form_farmer').id
                menu = request.env.ref('farmer.menu_farmer_form_submenu1').id
                model = request.env.ref('farmer.model_farm_farmer').id
                return request.redirect('/web#id=%s&cids=1&menu_id=%s&action=%s&model=%s&view_type=form'%(str(farmer_id),menu,action,model))
            except:
                return request.redirect('/my/home')
        if household_id:
            try:
                action = request.env.ref('farmer.action_form_household').id
                menu = request.env.ref('farmer.menu_farmer_form_submenu3').id
                model = request.env.ref('farmer.model_farm_household').id
                return request.redirect('/web#id=%s&cids=1&menu_id=%s&action=%s&model=%s&view_type=form'%(str(household_id),menu,action,model))
            except:
                return request.redirect('/my/home')
        if farmer_group_id:
            try:
                action = request.env.ref('farmer.action_form_farmer_group').id
                menu = request.env.ref('farmer.menu_farmer_form_submenu2').id
                model = request.env.ref('farmer.model_farmer_group').id
                return request.redirect('/web#id=%s&cids=1&menu_id=%s&action=%s&model=%s&view_type=form'%(str(farmer_group_id),menu,action,model))
            except:
                return request.redirect('/my/home')
