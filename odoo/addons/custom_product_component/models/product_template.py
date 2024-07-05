from odoo import models, fields, api


class ProductTemplateComponentRel(models.Model):
    _name = 'product.template.component.rel'
    _description = 'Product Template Component Relation'

    product_template_id = fields.Many2one('product.template', string='Product Template', required=True)
    product_component_id = fields.Many2one('product.component', string='Product Component', required=True)
    value_type = fields.Selection([
        ('value_range', 'Value Range'),
        ('fix_value', 'Fix Value')],
        string='Component Value', required=True, default='value_range')
    min_value = fields.Float(string='Min Value (in %)', digits=(12, 3))
    max_value = fields.Float(string='Max / Fixed Value (in %)', digits=(12, 3))


class ProductTemplateChemicalComponentRel(models.Model):
    _name = 'product.template.chemical.component.rel'
    _description = 'Product Template Chemical Component Relation'

    template_id = fields.Many2one('product.template', string='Product Template', required=True)
    product_component_id = fields.Many2one('chemical.component', string='Chemical Component', required=True)
    value_type = fields.Selection([
        ('value_range', 'Value Range'),
        ('fix_value', 'Fix Value')],
        string='Component Value', required=True, default='value_range')
    min_value = fields.Float(string='Min Value (in %)', digits=(12, 3))
    max_value = fields.Float(string='Max / Fixed Value (in %)', digits=(12, 3))
    price = fields.Float(string='Price')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    component_ids = fields.One2many('product.template.component.rel', 'product_template_id',
                                    string='Product Components')
    chemical_component_ids = fields.One2many('product.template.chemical.component.rel', 'template_id',
                                             string='Chemical Components')
