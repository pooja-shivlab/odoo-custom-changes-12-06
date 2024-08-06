from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')

    @api.onchange('purchase_order_id')
    def _onchange_purchase_order_id(self):
        if self.purchase_order_id:
            # Clear existing order lines
            self.order_line = [(5, 0, 0)]

            # Fetch the purchase order lines
            po_lines = self.purchase_order_id.order_line

            # Create sale order lines from purchase order lines
            sale_order_lines = []
            for line in po_lines:
                sale_order_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_qty,
                    'price_unit': line.price_unit,
                    'name': line.name,
                }))

            self.order_line = sale_order_lines
