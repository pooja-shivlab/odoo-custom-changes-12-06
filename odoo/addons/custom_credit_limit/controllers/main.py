from odoo import http
from odoo.http import request


class PartnerOverviewController(http.Controller):

    @http.route('/partner_overview', type='http', auth='public', website=True)
    def partner_overview_page(self, **kwargs):
        return request.render('custom_credit_limit.partner_overview')


class CustomNotificationController(http.Controller):
    @http.route('/web/dataset/call_kw/sale.order/get_credit_limit_warnings', type='json', auth='user')
    def get_credit_limit_warnings(self):
        SaleOrder = request.env['sale.order']
        print("000000000000000000000000", SaleOrder)
        warnings = SaleOrder.get_credit_limit_warnings()
        return {'result': warnings}
