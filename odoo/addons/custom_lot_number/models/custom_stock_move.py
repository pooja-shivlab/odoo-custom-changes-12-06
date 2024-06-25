from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    lot_name = fields.Char('Lot/Serial Number', compute='_compute_lot_name')

    @api.depends('lot_ids.name')
    def _compute_lot_name(self):
        for move in self:
            lot_names = move.lot_ids.mapped('name')
            move.lot_name = ', '.join(filter(None, lot_names)) if lot_names else ''
