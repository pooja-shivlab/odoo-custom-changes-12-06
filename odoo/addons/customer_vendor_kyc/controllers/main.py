from odoo import http
from odoo.http import request


class CustomerFormController(http.Controller):

    @http.route('/customer/form/<token>', auth='public', website=True)
    def customer_form(self, token=None, **kwargs):
        form = request.env['customer.details.form'].sudo().search([('token', '=', token)])
        if form:
            return request.render('customer_vendor_kyc.customer_form_template', {
                'form': form,
            })
        else:
            return "Sorry! Form submission failed. Please try again."

    @http.route('/customer/form/submit', type='http', auth='public', methods=['POST'], website=True)
    def customer_form_submit(self, **post):
        form_id = post.get('form_id')
        preferred_email = post.get('preferred_email')

        form = request.env['customer.details.form'].sudo().browse(int(form_id))
        if form:
            form.write({'preferred_email': preferred_email})
            return "Thank you for submitting your preferred email address!"
        else:
            return "Form submission failed. Please try again."
