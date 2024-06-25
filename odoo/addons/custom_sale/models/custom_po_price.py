from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purchase_packaging_id = fields.Many2one('product.packaging', string='Packaging')
    purchase_packaging_qty = fields.Float(string='Packaging Quantity', compute='_compute_purchase_packaging_qty')

    calculated_component_price = fields.Float(string='Calculated Component Price',
                                              compute='_compute_calculated_component_price', store=True)

    @api.depends('product_id', 'product_uom_qty', 'purchase_packaging_id')
    def _compute_calculated_component_price(self):
        for line in self:
            if line.product_id:
                # Calculate the component price by summing the prices of the chemical components
                component_price_total = sum(
                    component.price for component in line.product_id.product_tmpl_id.chemical_component_ids)
                line.calculated_component_price = component_price_total

                if line.purchase_packaging_id:
                    # If packaging is specified, calculate price based on quantity and component price
                    line.price_unit = line.calculated_component_price * line.product_uom_qty
                else:
                    # If no packaging, component price is the price of the unit
                    line.price_unit = line.calculated_component_price
            else:
                line.calculated_component_price = 0.0
                line.price_unit = 0.0

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                # Return packaging domain based on selected product
                line._compute_calculated_component_price()
                return {'domain': {'purchase_packaging_id': [('product_id', '=', line.product_id.id)]}}
            else:
                return {'domain': {'purchase_packaging_id': []}}

    @api.depends('product_uom_qty', 'purchase_packaging_id')
    def _compute_purchase_packaging_qty(self):
        for line in self:
            if line.purchase_packaging_id:
                units_per_packaging = line.purchase_packaging_id.qty
                if units_per_packaging:
                    line.purchase_packaging_qty = line.product_uom_qty / units_per_packaging
                else:
                    line.purchase_packaging_qty = 0
            else:
                line.purchase_packaging_qty = 0
            # Compute the component price and set the unit price
            line._compute_calculated_component_price()

    @api.onchange('product_id', 'product_uom_qty', 'purchase_packaging_id')
    def _onchange_product_uom_qty(self):
        for line in self:
            if line.product_id and line.purchase_packaging_id:
                units_per_packaging = line.purchase_packaging_id.qty
                product_uom = line.product_uom.name
                if units_per_packaging and line.product_uom_qty % units_per_packaging != 0:
                    warning = {
                        'title': "Warning",
                        'message': ("This product is packaged by %.2f %s. You should buy %.2f %s." %
                                    (units_per_packaging, product_uom, units_per_packaging, product_uom))
                    }
                    return {'warning': warning}
            # Compute the component price and set the unit price
            line._compute_calculated_component_price()
