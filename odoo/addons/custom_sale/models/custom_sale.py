from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_id = fields.Many2one('purchase.order', string='Select Purchase Order')
