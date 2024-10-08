{
    'name': 'Custom Credit Limit',
    'version': '1.0',
    'summary': 'Manage to show notifications',
    'depends': ['base', 'web', 'sale', 'account', 'custom_sale'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_partner_overview_template.xml',
        'views/report_partner_overview_view.xml',
        'views/partner_overview.xml',
        'views/res_partner_credit_limit_views.xml',
        'views/sale_order_views.xml',
    ],
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
