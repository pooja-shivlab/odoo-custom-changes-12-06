from odoo import http
from odoo.http import request


class PartnerOverviewController(http.Controller):

    @http.route('/partner_overview', type='http', auth='public', website=True)
    def partner_overview_page(self, **kwargs):
        return request.render('custom_credit_limit.partner_overview')
