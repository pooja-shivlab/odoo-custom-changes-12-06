from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', string='Sales Order')

    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            # Clear existing order lines
            self.order_line = [(5, 0, 0)]

            # Fetch the sale order lines
            sale_order_lines = self.sale_order_id.order_line

            # Create purchase order lines from sale order lines
            po_lines = []
            for line in sale_order_lines:
                po_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'name': line.name,
                }))
            self.order_line = po_lines
