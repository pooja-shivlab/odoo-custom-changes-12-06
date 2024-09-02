from odoo import http
from odoo.http import request
import json


class PartnerOverviewController(http.Controller):

    @http.route('/partner_overview', type='http', auth='public', website=True)
    def partner_overview_page(self, **kwargs):
        return request.render('custom_credit_limit.partner_overview')


class CustomNotificationController(http.Controller):
    @http.route('/web/dataset/call_kw/sale.order/get_credit_limit_warnings', type='json', auth='user')
    def get_credit_limit_warnings(self, **kwargs):
        raw_data = request.httprequest.get_data(as_text=True)

        # Parse the JSON data
        try:
            params = json.loads(raw_data)
        except json.JSONDecodeError:
            params = {}

        customer = params.get('customer')
        type = params.get('type')
        SaleOrder = request.env['sale.order']
        warnings = SaleOrder.get_credit_limit_warnings(type, customer)
        return {'result': warnings}
