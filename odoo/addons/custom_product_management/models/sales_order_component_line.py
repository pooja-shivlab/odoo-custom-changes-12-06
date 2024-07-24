from odoo import models, fields, api


class SaleProductComponentLines(models.Model):
    _name = 'sale.product.component.lines'
    _description = 'Sale Product Component Lines'

    product_component_id = fields.Many2one('product.component', string='Product Component', required=True)
    sale_order_component_id = fields.Many2one('sale.order.components', string='Sale Order Component',
                                              ondelete='cascade')
    product_tmpl_id = fields.Many2one('product.template', string='Product Template')
    price_editable = fields.Boolean(string='Is Price Editable', default=False)
    value_type = fields.Selection([
        ('value_range', 'Value Range'),
        ('fix_value', 'Fix Value')],
        string='Component Value', required=True, default='value_range')
    min_value = fields.Float(string='Min Value (in %)', digits=(12, 3))
    max_value = fields.Float(string='Max / Fixed Value (in %)', digits=(12, 3))
    price = fields.Float(string='Price')


class SaleChemicalComponentLines(models.Model):
    _name = 'sale.chemical.component.lines'
    _description = 'Sale Chemical Component Lines'

    chemical_component_id = fields.Many2one('chemical.component', string='Chemical Component', required=True)
    sale_order_chemical_component_id = fields.Many2one('sale.order.components', string='Sale Order Chemical Component',
                                                       ondelete='cascade')
    product_tmpl_id = fields.Many2one('product.template', string='Product Template')
    price_editable = fields.Boolean(string='Is Price Editable', default=False)
    value_type = fields.Selection([
        ('value_range', 'Value Range'),
        ('fix_value', 'Fix Value')],
        string='Component Value', required=True, default='value_range')
    min_value = fields.Float(string='Min Value (in %)', digits=(12, 3))
    max_value = fields.Float(string='Max / Fixed Value (in %)', digits=(12, 3))
    price = fields.Float(string='Price')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    component_line_ids = fields.One2many('sale.product.component.lines', 'product_tmpl_id', string='Product Components')
    chemical_component_line_ids = fields.One2many('sale.chemical.component.lines', 'product_tmpl_id',
                                                  string='Chemical Components')


class SaleOrderComponents(models.Model):
    _name = 'sale.order.components'
    _description = 'Sale Order Components'

    price_editable = fields.Boolean(string='Is Price Editable', default=False)
    product_component_line_ids = fields.One2many('sale.product.component.lines', 'sale_order_component_id',
                                                 string='Product Components')
    product_chemical_line_ids = fields.One2many('sale.chemical.component.lines', 'sale_order_chemical_component_id',
                                                string='Chemical Components')
    order_id = fields.Many2one('sale.order', string='Sales Order')
    sale_line_id = fields.Many2one('sale.order.line', string='Sales Order Lines')
    po_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    po_line_id = fields.Many2one('purchase.order.line', string='Purchase Order Lines')
    product_id = fields.Many2one('product.product', string='Product')
    product_tmpl_id = fields.Many2one('product.template', string='Product Template')

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderComponents, self).default_get(fields)
        product_tmpl_id = self._context.get('default_product_template_id')
        sale_line_id = self._context.get('default_sale_order_line_id')

        if product_tmpl_id and sale_line_id:
            sale_order_components = self.search([
                ('product_tmpl_id', '=', product_tmpl_id),
                ('sale_line_id', '=', sale_line_id)
            ], order='create_date desc', limit=1)

            if sale_order_components:
                product_component_lines = []
                for line in sale_order_components.product_component_line_ids:
                    product_component_lines.append((0, 0, {
                        'product_component_id': line.product_component_id.id,
                        'price_editable': line.price_editable,
                        'value_type': line.value_type,
                        'min_value': line.min_value,
                        'max_value': line.max_value,
                    }))

                product_chemical_lines = []
                for line in sale_order_components.product_chemical_line_ids:
                    product_chemical_lines.append((0, 0, {
                        'chemical_component_id': line.chemical_component_id.id,
                        'price_editable': line.price_editable,
                        'value_type': line.value_type,
                        'min_value': line.min_value,
                        'max_value': line.max_value,
                        'price': line.price,
                    }))

                res.update({
                    'price_editable': sale_order_components.price_editable,
                    'product_component_line_ids': product_component_lines,
                    'product_chemical_line_ids': product_chemical_lines,
                    'order_id': sale_order_components.order_id.id,
                    'sale_line_id': sale_order_components.sale_line_id.id,
                    'po_order_id': sale_order_components.po_order_id.id,
                    'po_line_id': sale_order_components.po_line_id.id,
                    'product_id': sale_order_components.product_id.id,
                    'product_tmpl_id': sale_order_components.product_tmpl_id.id,
                })
            else:
                # Load default components from the product template
                product_component_lines = []
                product_chemical_lines = []
                product_template = self.env['product.template'].browse(product_tmpl_id)

                for rel in product_template.component_line_ids:
                    product_component_lines.append((0, 0, {
                        'product_component_id': rel.product_component_id.id,
                        'value_type': rel.value_type,
                        'min_value': rel.min_value,
                        'max_value': rel.max_value,
                    }))

                for rel in product_template.chemical_component_line_ids:
                    product_chemical_lines.append((0, 0, {
                        'chemical_component_id': rel.chemical_component_id.id,
                        'value_type': rel.value_type,
                        'min_value': rel.min_value,
                        'max_value': rel.max_value,
                        'price': rel.price,
                    }))
                res['product_tmpl_id'] = product_template.id
                res['sale_line_id'] = sale_line_id
                res['product_component_line_ids'] = product_component_lines
                res['product_chemical_line_ids'] = product_chemical_lines
        return res

    def save_changes(self):
        # Save changes to product components
        for line in self.product_component_line_ids:
            component_line = self.env['sale.product.component.lines'].search([
                ('sale_order_component_id', '=', self.id),
                ('product_component_id', '=', line.product_component_id.id)
            ], limit=1)

            if component_line:
                component_line.write({
                    'price_editable': line.price_editable,
                    'value_type': line.value_type,
                    'min_value': line.min_value,
                    'max_value': line.max_value,
                })
            else:
                self.env['sale.product.component.lines'].create({
                    'product_tmpl_id': self.product_tmpl_id.id,
                    'sale_line_id': self.sale_line_id.id,
                    'sale_order_component_id': self.id,
                    'product_component_id': line.product_component_id.id,
                    'price_editable': line.price_editable,
                    'value_type': line.value_type,
                    'min_value': line.min_value,
                    'max_value': line.max_value,
                })

        # Save changes to chemical components
        for line in self.product_chemical_line_ids:
            chemical_line = self.env['sale.chemical.component.lines'].search([
                ('sale_order_chemical_component_id', '=', self.id),
                ('chemical_component_id', '=', line.chemical_component_id.id)
            ], limit=1)

            if chemical_line:
                chemical_line.write({
                    'price_editable': line.price_editable,
                    'value_type': line.value_type,
                    'min_value': line.min_value,
                    'max_value': line.max_value,
                    'price': line.price,
                })
            else:
                self.env['sale.chemical.component.lines'].create({
                    'product_tmpl_id': self.product_tmpl_id.id,
                    'sale_line_id': self.sale_line_id.id,
                    'sale_order_chemical_component_id': self.id,
                    'chemical_component_id': line.chemical_component_id.id,
                    'price_editable': line.price_editable,
                    'value_type': line.value_type,
                    'min_value': line.min_value,
                    'max_value': line.max_value,
                    'price': line.price,
                })
