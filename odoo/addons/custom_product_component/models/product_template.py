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


class SaleOrderLineComponentRel(models.Model):
    _name = 'sale.order.line.component.rel'
    _description = 'Sales Order Line Component Relation'

    component_ids = fields.One2many('product.component.rel', 'component_ids', string='Components')
    chemical_component_ids = fields.One2many('chemical.component.rel', 'component_ids', string='Chemical Components')
    product_template_id = fields.Many2one('product.template', string='Product Template', required=True)
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', required=True)
    is_checked = fields.Boolean(string='Is Checked', default=False)

    @api.model
    def default_get(self, fields):
        defaults = super(SaleOrderLineComponentRel, self).default_get(fields)
        if self._context.get('default_product_template_id') and self._context.get('default_sale_order_line_id'):
            product_template_id = self._context['default_product_template_id']
            sale_order_line_id = self._context['default_sale_order_line_id']
            defaults['product_template_id'] = product_template_id
            defaults['sale_order_line_id'] = sale_order_line_id

            # Check if there are existing components for this sale order line
            existing_components = self.search([
                ('product_template_id', '=', product_template_id),
                ('sale_order_line_id', '=', sale_order_line_id)
            ], order='create_date desc', limit=1)

            if existing_components:
                component_defaults = []
                chemical_component_defaults = []
                for rel in existing_components.component_ids:
                    component_defaults.append((0, 0, {
                        'product_component_id': rel.product_component_id.id,
                        'value_type': rel.value_type,
                        'min_value': rel.min_value,
                        'max_value': rel.max_value,
                    }))
                for rel in existing_components.chemical_component_ids:
                    chemical_component_defaults.append((0, 0, {
                        'product_component_id': rel.product_component_id.id,
                        'value_type': rel.value_type,
                        'min_value': rel.min_value,
                        'max_value': rel.max_value,
                        'price': rel.price,
                    }))
                defaults['component_ids'] = component_defaults
                defaults['chemical_component_ids'] = chemical_component_defaults
            else:
                # Load default components from the product template
                component_defaults = []
                chemical_component_defaults = []
                product_template = self.env['product.template'].browse(product_template_id)
                for rel in product_template.component_ids:
                    component_defaults.append((0, 0, {
                        'product_component_id': rel.product_component_id.id,
                        'value_type': rel.value_type,
                        'min_value': rel.min_value,
                        'max_value': rel.max_value,
                    }))
                for rel in product_template.chemical_component_ids:
                    chemical_component_defaults.append((0, 0, {
                        'product_component_id': rel.product_component_id.id,
                        'value_type': rel.value_type,
                        'min_value': rel.min_value,
                        'max_value': rel.max_value,
                        'price': rel.price,
                    }))
                defaults['component_ids'] = component_defaults
                defaults['chemical_component_ids'] = chemical_component_defaults

        return defaults

    def save_changes(self):
        for component in self.component_ids:
            vals = {
                'component_ids': self.id,
                'product_component_id': component.product_component_id.id,
                'value_type': component.value_type,
                'min_value': component.min_value,
                'max_value': component.max_value,
            }
            existing_component = self.env['product.component.rel'].search([
                ('component_ids', '=', self.id),
                ('product_component_id', '=', component.product_component_id.id),
            ])
            if existing_component:
                existing_component.write(vals)
            else:
                self.env['product.component.rel'].create(vals)

        for component in self.chemical_component_ids:
            vals = {
                'component_ids': self.id,
                'product_component_id': component.product_component_id.id,
                'value_type': component.value_type,
                'min_value': component.min_value,
                'max_value': component.max_value,
                'price': component.price,
            }
            existing_component = self.env['chemical.component.rel'].search([
                ('component_ids', '=', self.id),
                ('product_component_id', '=', component.product_component_id.id),
            ])
            if existing_component:
                existing_component.write(vals)
            else:
                self.env['chemical.component.rel'].create(vals)


class ProductComponentRel(models.Model):
    _name = 'product.component.rel'
    _description = 'Product Component Relation'

    component_ids = fields.Many2one('sale.order.line.component.rel', string='Components', required=True,
                                    ondelete='cascade')
    product_component_id = fields.Many2one('product.component', string='Product Component', required=True)
    value_type = fields.Selection([
        ('value_range', 'Value Range'),
        ('fix_value', 'Fix Value')],
        string='Component Value', required=True, default='value_range')
    min_value = fields.Float(string='Min Value (in %)', digits=(12, 3))
    max_value = fields.Float(string='Max / Fixed Value (in %)', digits=(12, 3))


class SaleOrderLineChemicalComponentRel(models.Model):
    _name = 'chemical.component.rel'
    _description = 'Chemical Component Relation'

    component_ids = fields.Many2one('sale.order.line.component.rel', string='Components', required=True,
                                    ondelete='cascade')
    product_component_id = fields.Many2one('chemical.component', string='Chemical Component', required=True)
    value_type = fields.Selection([
        ('value_range', 'Value Range'),
        ('fix_value', 'Fix Value')],
        string='Component Value', required=True, default='value_range')
    min_value = fields.Float(string='Min Value (in %)', digits=(12, 3))
    max_value = fields.Float(string='Max / Fixed Value (in %)', digits=(12, 3))
    price = fields.Float(string='Price')
