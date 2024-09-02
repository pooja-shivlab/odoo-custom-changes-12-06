from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    reminder_interval_number = fields.Integer(
        string="KYC Reminder After",
        default=0,
    )
    reminder_interval_type = fields.Selection(
        [('days', 'Days'), ('hours', 'Hours')],
        string="Reminder Interval Type",
        default='days',
    )

    token_expire_interval_number = fields.Integer(
        string="Token Expiry After",
        default=0,
    )

    token_expire_interval_type = fields.Selection(
        [('days', 'Days'), ('hours', 'Hours')],
        string="Token Expiry Interval Type",
        default='days',
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'reminder_interval_number', self.reminder_interval_number
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'reminder_interval_type', self.reminder_interval_type
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'token_expire_interval_number', self.token_expire_interval_number
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'token_expire_interval_type', self.token_expire_interval_type
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['reminder_interval_number'] = int(
            self.env['ir.config_parameter'].sudo().get_param('reminder_interval_number', default=0)
        )
        res['reminder_interval_type'] = self.env['ir.config_parameter'].sudo().get_param(
            'reminder_interval_type', default='days'
        )
        res['token_expire_interval_number'] = int(
            self.env['ir.config_parameter'].sudo().get_param('token_expire_interval_number', default=0)
        )
        res['token_expire_interval_type'] = self.env['ir.config_parameter'].sudo().get_param(
            'token_expire_interval_type', default='days'
        )
        return res
