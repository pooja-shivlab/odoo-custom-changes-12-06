{
    'name': 'Customer Vendor KYC',
    'version': '1.0',
    'summary': 'Add customer vendor kyc',
    'depends': [
        'base',
        'sale',
        'purchase',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_kyc_views.xml',
        'data/mail_template_data.xml',
        'views/customer_details_form_views.xml',
        'views/customer_form.xml',
        'views/vendor_form.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'customer_vendor_kyc/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}