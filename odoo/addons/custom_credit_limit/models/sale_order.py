from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.customer_credit_limit = self.partner_id.customer_credit_limit
            self.blocking_limit = self.partner_id.blocking_limit

    customer_credit_limit = fields.Float(related='partner_id.customer_credit_limit', string='Credit Limit',
                                         readonly=True)
    blocking_limit = fields.Float(related='partner_id.blocking_limit', string='Blocking Limit', readonly=True)
