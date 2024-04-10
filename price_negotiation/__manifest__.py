# -*- coding: utf-8 -*-
{
    'name': "price_negotiation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Damodar Aryal & Utsab Bardewa",
    'application':True,
    'sequence': 1,
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','utm','website_sale','portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'views/views.xml',
        'views/menu_negotiation_extension.xml',
        'data/template_inheritance.xml',
        # 'data/portal_template_inheritance.xml',
        'data/email_template.xml',
        'data/sequence_data.xml',
        'views/price_negotiation_views.xml',
        'views/counter_price_popup.xml',
        # 'views/negotiation_popup_form_template.xml',
        'views/price_negotiation_template.xml',
        # 'views/modal_template.xml',
        # 'views/test.xml',
        # 'models/models.py'

        'views/templates.xml',
    ],
    'assets':{

        'web.assets_frontend':[
            'price_negotiation/static/src/js/negotiation_request_form.js'
        ],
    }
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
