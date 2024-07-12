from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_due_amount = fields.Text(compute='_compute_customer_due_amount', store=False, readonly=True)

    @api.depends('partner_id')
    def _compute_customer_due_amount(self):
        for order in self:
            if order.partner_id:
                # Implement your logic to calculate the due amount
                due_amount = 0.0  # Placeholder, replace with your actual logic
                order.customer_due_amount = "The Customer's Due Amount is $ {:.2f}".format(due_amount)
            else:
                order.customer_due_amount = ""

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self._compute_customer_due_amount()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.customer_credit_limit = self.partner_id.customer_credit_limit
            self.blocking_limit = self.partner_id.blocking_limit

    customer_credit_limit = fields.Float(related='partner_id.customer_credit_limit', string='Credit Limit',
                                         readonly=True)
    blocking_limit = fields.Float(related='partner_id.blocking_limit', string='Blocking Limit', readonly=True)
