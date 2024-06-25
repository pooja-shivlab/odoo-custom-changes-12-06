{
    'name': 'Custom Sale Order',
    'version': '1.0',
    'summary': 'Adds custom fields to sale orders',
    'depends': [
        'base',
        'product',
        'sale',
        'purchase',
        'analytic',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_packaging_views.xml',
        'views/custom_sale_views.xml',
        'views/custom_purchase_views.xml',
        'views/purchase_packaging_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}