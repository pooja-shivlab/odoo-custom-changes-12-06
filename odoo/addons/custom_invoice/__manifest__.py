{
    'name': 'Custom Invoice',
    'version': '1.0',
    'summary': 'Custom Invoice Report',
    'depends': ['base', 'account'],
    'data': [
        'report/report_invoice_template.xml',
        'views/report_invoice_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
