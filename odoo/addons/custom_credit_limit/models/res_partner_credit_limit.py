from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_credit_limit = fields.Float(string='Customer Credit Limit', default=0.0)
    blocking_limit = fields.Float(string='Blocking Limit', default=0.0)
