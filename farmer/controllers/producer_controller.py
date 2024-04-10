from odoo import http
from odoo.http import request
import json

class FarmerForm(http.Controller):

    @http.route('/farmer_form', type='http', website=True, auth="public")
    def submit_form(self, **kw):
            return request.render('farmer.farmer_form_template', {})


    @http.route('/create/farmer_record', type='http', website=True, auth="public", Methods=['POST'])
    def create_form(self, **kw):
        if len(kw)==0:
            return request.render('farmer.farmer_form_template', {})

        data = json.loads(kw['one2many_data'])
        # val = [(0, 0, line) for line in data]
        print(data)
        print(kw)
        values = {
            'name': kw['name'],
            'citizenship_issue_district':int(kw['citizenship_issue_district'])
        }
        for field in data:
            for line in data[field]:
                for key in line:
                    if line[key].isdigit():
                        line[key]=int(line[key])
            print(field)
            values[field]=[(0,0,line) for line in data[field]]
        print(values)
        form_id = request.env['farm.farmer'].sudo().create(values)
        print(form_id)
        return request.render('farmer.farmer_form_template', {})

class FarmerGroupForm(http.Controller):

    @http.route('/farmer_group_form', type='http', website=True, auth="public")
    def submit_form(self, **kw):
            return request.render('farmer.farmer_group_form_template', {})

    @http.route('/create/farmer_group_record', type='http', website=True, auth="public", Methods=['POST'])
    def create_form(self, **kw):
        if len(kw)==0:
            return request.render('farmer.farmer_group_form_template', {})

        data = json.loads(kw['one2many_data'])
        values = {
            'name': kw['name'],
        }
        # typecasting to int
        for field in data:
            for line in data[field]:
                for key in line:
                    if line[key].isdigit():
                        line[key]=int(line[key])
            values[field]=[(0,0,line) for line in data[field]]
        form_id = request.env['farmer.group'].sudo().create(values)
        return request.render('farmer.farmer_group_form_template', {})


class HouseholdrForm(http.Controller):

    @http.route('/household_form', type='http', website=True, auth="public")
    def submit_form(self, **kw):
            return request.render('farmer.household_form_template', {})
