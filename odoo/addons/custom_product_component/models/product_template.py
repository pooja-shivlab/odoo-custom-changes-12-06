from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    chemical_component_ids = fields.One2many('chemical.component', 'product_id', string='Chemical Components')
    pricing_ids = fields.One2many('chemical.component', 'product_id', string='Pricing')
