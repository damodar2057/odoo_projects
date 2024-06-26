{
    "name": "farmer_app",
    "author": "Bbox",
    "version": "1.0.1.0.0",
    "category": "",
    'application': True,
    'sequence': 1,
    'depends': ['base','website','website_sale','utm','stock'],
    'data': [
        'security/user_group_access.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/farmer_data.xml',
        'data/farmer_type_data.xml',
        'data/res_lang_data.xml',
        'data/local_production_category_default_data.xml',
        'data/farmer_id.xml',
        'data/email_templates/email_template_approved.xml',
        'data/email_templates/email_template_create.xml',
        'data/email_templates/email_template_declined.xml',
        'data/email_templates/email_template_onhold.xml',
        'data/organization_type_data.xml',
        'views/farmer_menu.xml',
        'views/farmer_request_views.xml',
        'views/farmer_info_views.xml',
        'views/farmer_group_views.xml',
        'views/household_info_views.xml',
        'views/farmer_group_poc_views.xml',
        'views/farmer_crop_views.xml',
        'views/farmer_land_views.xml',
        'views/farmer_fish_views.xml',
        'views/farmer_animal_views.xml',
        'views/farmer_documents_views.xml',
        'views/farmer_loan_views.xml',
        'views/farmer_associated_institute_views.xml',
        'views/farmer_family_members_views.xml',
        'views/household_local_production_views.xml',
        'views/organization_views.xml',
        
        'views/configuration_agriculture_views.xml',
        'views/configuration_loans_and_institution_views.xml',
        'views/configuration_services_views.xml',
        'views/configuration_others_views.xml',
        'views/configuration_location_views.xml',
        'views/configuration_programs_views.xml',
        'views/configuration_family_member_attributes_views.xml',
        'views/configuration_speciality_views.xml',
        # 'views/website_menu.xml',
        # 'views/farmer_group_form_template.xml',
        # 'views/farmer_form_template.xml',
        'views/website_request_menu.xml',
        # 'views/request_form_template.xml',
        'views/profile_update_request_view.xml',
        'views/farmer_type.xml',
        'views/specialist_views.xml',
        'views/farmer_group_metadata.xml',
        'views/farmer_group_members_views.xml',
        'views/produce_insurance_views.xml',
        'views/freezer_location_views.xml',
        'views/configuration_organization.xml',
        'data/province_data.xml',
        'data/district_data.xml',
        'data/palika_data.xml',
        ],

        'assets':{
            'web.assets_frontend': [
                "farmer/static/src/js/website_form.js",
                "farmer/static/src/scss/website_form.scss",
            ],
            'web.assets_backend': [
                "farmer/static/src/css/farmer.css",
                # "farmer/static/src/js/styler.js",
            ],
            'web.report_assets_common':[
                "farmer/static/src/css/style.css",
            ]
        },
}



