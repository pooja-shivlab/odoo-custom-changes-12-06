from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    contract_no = fields.Char(String="Contract No")
    supplier_no = fields.Char(String="Supplier No")

    def action_report_nimet_invoice(self):
        return self.env.ref('custom_invoice.account_nimet_invoice').report_action(self)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    bol_number = fields.Char(String="BOL Number")
