{
    'name': 'Custom Product Management',
    'version': '1.0',
    'summary': 'Adds custom fields to product',
    'depends': [
        'base', 'web', 'product', 'stock', 'sale', 'custom_product_component', 'purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/sales_order_component_line.xml',
        'views/sales_order_component_popup.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
