{
    'name': 'Customer Vendor KYC',
    'version': '1.0',
    'summary': 'Add customer vendor kyc',
    'depends': [
        'base',
        'sale',
        'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_kyc_views.xml',
        'data/mail_template_data.xml',
        'views/customer_details_form_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}