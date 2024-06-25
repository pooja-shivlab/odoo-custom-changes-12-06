from odoo import models, fields, api
import uuid


class CustomerDetailsForm(models.Model):
    _name = 'customer.details.form'
    _description = 'Customer Details Form'

    customer_id = fields.Many2one('res.partner', string='Customer')
    token = fields.Char(string='Token', readonly=True)
    preferred_email = fields.Char(string='Preferred email address for invoices')

    @api.model
    def create(self, vals):
        # Generate a unique token
        vals['token'] = uuid.uuid4().hex
        return super(CustomerDetailsForm, self).create(vals)
