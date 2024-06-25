{
    'name': 'Custom Lot Number',
    'version': '1.0',
    'summary': 'Manage to show lot number',
    'depends': [
        'product',
        'stock',
    ],
    'data': [
        'views/custom_stock_picking_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
