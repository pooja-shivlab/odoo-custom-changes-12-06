from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_credit_limit = fields.Monetary(
        related='partner_id.customer_credit_limit',
        string='Credit Limit',
        readonly=True,
        currency_field='currency_id'
    )
    blocking_limit = fields.Monetary(
        related='partner_id.blocking_limit',
        string='Blocking Limit',
        readonly=True,
        currency_field='currency_id'
    )
    receivable_amount = fields.Monetary(
        compute='_compute_receivable_amount',
        string='Total Receivable',
        readonly=True
    )
    customer_credit_warning = fields.Text(
        compute='_compute_customer_credit_warning',
        groups="account.group_account_invoice,account.group_account_readonly"
    )
    is_warning = fields.Boolean()

    @api.depends('partner_id', 'amount_total', 'state')
    def _compute_receivable_amount(self):
        for order in self:
            partner = order.partner_id.commercial_partner_id if order.partner_id else None
            if partner and partner.customer_credit_limit > 0:
                receivable_orders = self.env['sale.order'].search([
                    ('partner_id', '=', partner.id),
                    ('state', 'in', ['draft', 'sent', 'sale', 'done'])
                ])
                order.receivable_amount = sum(receivable_orders.mapped('amount_total'))
            else:
                order.receivable_amount = 0.0

    @api.depends('partner_id', 'receivable_amount')
    def _compute_customer_credit_warning(self):
        for order in self:
            order.customer_credit_warning = ''
            order.is_warning = False
            if order.partner_id:
                partner = order.partner_id.commercial_partner_id
                credit_limit = partner.customer_credit_limit
                if credit_limit and order.receivable_amount > credit_limit:
                    order.customer_credit_warning = _("The customer's credit limit has been crossed")
                    order.is_warning = True

    def action_confirm(self):
        for order in self:
            partner = order.partner_id.commercial_partner_id if order.partner_id else None
            if partner:
                blocking_limit = partner.blocking_limit
                if blocking_limit and order.receivable_amount > blocking_limit:
                    raise UserError(_("The customer has exceeded the blocking limit."))
            if order.customer_credit_warning:
                raise UserError(order.customer_credit_warning)
        return super(SaleOrder, self).action_confirm()

    @api.model
    def get_credit_limit_warnings(self):
        sale_orders = self.search([
            ('state', 'in', ['draft', 'sent', 'sale', 'done'])
        ])
        unique_warnings = set()  # To keep track of unique messages

        for order in sale_orders:
            order._compute_customer_credit_warning()  # Ensure computed field is updated
            if order.is_warning:
                if order.customer_credit_warning not in unique_warnings:
                    unique_warnings.add(order.customer_credit_warning)
                    return {'message': order.customer_credit_warning}
