{
    'name': 'Custom Credit Limit',
    'version': '1.0',
    'summary': 'Manage to show notifications',
    'depends': ['base', 'web'],
    'assets': {
            'web.assets_backend': [
                'custom_credit_limit/static/src/**/*',
            ],
     },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
