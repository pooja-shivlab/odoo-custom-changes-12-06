from odoo import models, fields


class ProductComponent(models.Model):
    _name = 'product.component'
    _description = 'Product Component'

    name = fields.Char(string='Component Name', required=True)
    short_name = fields.Char(string='Short Name')


class ChemicalComponent(models.Model):
    _name = 'chemical.component'
    _description = 'Chemical Component'

    product_id = fields.Many2one('product.template', string='Product', ondelete='cascade')
    component_id = fields.Many2one('product.component', string='Component')
    component_name = fields.Char(string='Component Name', related='component_id.name', store=True)
    value_type = fields.Selection([
        ('value_range', 'Value Range'),
        ('fix_value', 'Fix Value')],
        string='Component Value', required=True, default='value_range')
    min_value = fields.Float(string='Min Value (in %)')
    max_value = fields.Float(string='Max/Fixed Value (in %)')
    price = fields.Float(string='Price')
