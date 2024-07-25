from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def open_product_components_action(self):
        self.ensure_one()
        product_template = self.product_id.product_tmpl_id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Components',
            'res_model': 'sale.order.components',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('custom_product_management.view_sale_order_components_form').id,
            'context': {
                'default_product_template_id': product_template.id,
                'default_sale_order_line_id': self.id,
            },
        }


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def open_product_components_action(self):
        self.ensure_one()
        product_template = self.product_id.product_tmpl_id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Components',
            'res_model': 'sale.order.components',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('custom_product_management.view_sale_order_components_form').id,
            'context': {
                'default_product_template_id': product_template.id,
                'default_sale_order_line_id': self.id,
            },
        }
