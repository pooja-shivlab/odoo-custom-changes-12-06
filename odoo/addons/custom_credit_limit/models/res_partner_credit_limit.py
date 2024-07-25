from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_credit_limit = fields.Monetary(
        string='Customer Credit Limit',
        default=0.0,
        currency_field='currency_id'
    )
    blocking_limit = fields.Monetary(
        string='Blocking Limit',
        default=0.0,
        currency_field='currency_id'
    )
    total_receivable_amount = fields.Monetary(
        compute='_compute_total_receivable_amount',
        string='Total Receivable',
        readonly=True,
        currency_field='currency_id'
    )

    @api.depends('sale_order_ids.amount_total', 'sale_order_ids.state')
    def _compute_total_receivable_amount(self):
        for partner in self:
            if partner.customer_credit_limit > 0:
                receivable_orders = self.env['sale.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', 'in', ['draft', 'sent', 'sale', 'done'])
                ])
                partner.total_receivable_amount = sum(receivable_orders.mapped('amount_total'))
            else:
                partner.total_receivable_amount = 0.0
