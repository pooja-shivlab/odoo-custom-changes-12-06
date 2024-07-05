from odoo import models, fields, api


class ProductComponent(models.Model):
    _name = 'product.component'
    _description = 'Product Component'

    name = fields.Char(string='Name', required=True)
    short_name = fields.Char(string='Short Name')
    is_default = fields.Boolean(default=False, string='Default')

    def toggle_default(self, *args):
        for record in self:
            record.is_default = True

    def remove_toggle_default(self, *args):
        for record in self:
            record.is_default = False


class ChemicalComponent(models.Model):
    _name = 'chemical.component'
    _description = 'Chemical Component'

    name = fields.Char(string='Name', required=True)
    short_name = fields.Char(string='Short Name')
    is_default = fields.Boolean(default=False, string='Default')

    def toggle_default(self, *args):
        for record in self:
            record.is_default = True

    def remove_toggle_default(self, *args):
        for record in self:
            record.is_default = False
