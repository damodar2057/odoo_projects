# -*- coding: utf-8 -*-

{
    'name': 'Biometric Device Integration',
    'version': '16.0.1.1.0',
    'depends': ['base_setup', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/zk_machine_view.xml',
        'views/zk_machine_attendance_view.xml',
        # 'views/leave_request.xml',
        'data/download_data.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence':1
}
