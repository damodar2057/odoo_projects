# -*- coding: utf-8 -*-
{
    'name': "vehicle_tracking",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'application':True,
    'sequence':2,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': [
        'base',
        'web',
        'fleet',
        'stock',
        'website_sale'
        # Add other missing modules here
    ],
    'qweb': ['static/src/xml/new.xml'],

    'data': [
        'security/ir.model.access.csv',
        'demo/ir_config_parameter.xml',
        'data/ir_config_parameter.xml',
        'data/driver_group.xml',
        'data/sequence_data.xml',
        'data/schedular_action.xml',
        'data/email_template.xml',
        'views/res_config_settings_view.xml',
        'views/views.xml',
        'views/track_order_menu.xml',
        'views/view_inherit.xml',
        'views/fuel_view.xml',
        # 'views/custom_leaflet_map_view.xml',
        'views/templates.xml',
        'views/track_vehicle_registry.xml'
    ],
    'assets':{
        'web.assets_backend':[
            'vehicle_tracking/static/src/xml/vehicle_status_dashboard.xml',
            'vehicle_tracking/static/src/css/map3.css',
            'vehicle_tracking/static/src/js/initialize_leaflet.js',
            'vehicle_tracking/static/src/js/vehicle_status_dashboard.js',
            'vehicle_tracking/static/src/xml/track_vehicle_template.xml',
            'vehicle_tracking/static/src/css/map_vehicle_track.scss',
            'vehicle_tracking/static/src/js/initialize_for_vehicle_tracking.js',
            'vehicle_tracking/static/src/js/track_vehicle.js',
            # 'vehicle_tracking/static/src/js/calling_for_gps_device.js',

            # 'vehicle_tracking/static/src/css/web_view_leaflet_map.css',
            # 'vehicle_tracking/static/src/leaflet/leaflet.css',
            # 'vehicle_tracking/static/src/leaflet/leaflet.js',
            # 'vehicle_tracking/static/src/js/view_registry.js',
            # 'vehicle_tracking/static/src/js/map_view.js',
            # 'vehicle_tracking/static/src/js/map_renderer.js',


            # 'vehicle_tracking/static/src/js/location_pinpoint.js',
            # 'vehicle_tracking/static/src/xml/pinpoint_location_html.xml',
        ],
        'web.assets_frontend':[
            # 'vehicle_tracking/static/src/leaflet/leaflet.css',
            # 'vehicle_tracking/static/src/leaflet/leaflet.js',
            # 'vehicle_tracking/static/src/js/new.js',

        ]
    },

}
