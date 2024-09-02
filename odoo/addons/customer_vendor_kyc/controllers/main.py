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


class CustomController(http.Controller):
    @http.route('/customer_form/<string:token>', type='http', auth='public', website=True)
    def customer_form(self, token, **kw):
        partner = request.env['res.partner'].sudo().search([('token', '=', token)])
        if not partner:
            return request.not_found()

        return request.render('customer_vendor_kyc.customer_form', {
            'partner_name': partner.name,
            'partner_email': partner.email,
            'token': partner.token,
            'street': partner.street or '',
            'street2': partner.street2 or '',
            'city': partner.city or '',
            'state': partner.state_id.name if partner.state_id else '',
            'country': partner.country_id.name if partner.country_id else '',
            'phone_number': partner.phone or '',
            'vat_number': partner.gst_hst_number or '',
            'company_website': partner.website or '',
            'business_start_date': partner.date or '',
            'registration_number': partner.registration_number or '',
            'country_parent_company': partner.country_parent_company or '',
            'type_of_business': partner.type_of_business or '',
            'annual_sales': partner.annual_sales or '',
            'place_of_corporation': partner.place_of_corporation or '',
            'parent_company': partner.parent_company or '',
            'years_ownership': partner.years_under_current_ownership or '',
            'number_locations': partner.number_of_location or '',
            'fiscal_year_end': partner.fiscal_years_end_date or '',
            'partner_completed_by': partner.partner_completed_by or '',
            'digital_sign_date': partner.digital_sign_date or '',
            'trade_currency': partner.trade_currency or '',
            'designation': partner.designation or '',
        })

    @http.route('/vendor_form/<string:token>', type='http', auth='public', website=True)
    def vendor_form(self, token, **kw):
        vendor = request.env['res.partner'].sudo().search([('token', '=', token)])
        if not vendor:
            return request.not_found()

        return request.render('customer_vendor_kyc.vendor_form', {
            'vendor_name': vendor.name,
            'vendor_email': vendor.email,
            'token': vendor.token,
            'street': vendor.street or '',
            'street2': vendor.street2 or '',
            'city': vendor.city or '',
            'state': vendor.state_id.name if vendor.state_id else '',
            'postal_code': vendor.zip or '',
            'country': vendor.country_id.name if vendor.country_id else '',
            'phone_number': vendor.phone or '',
            'ext_number': vendor.ext_number or '',
            'vendor_po_box': vendor.vendor_po_box or '',
            'vendor_fax': vendor.vendor_fax or '',
            'email_for_order': vendor.email_for_order or '',
            'order_template_number': vendor.order_template_number or '',
            'quebec_tax_number': vendor.quebec_tax_number or '',
            'irs_number': vendor.irs_number or '',
            'order_currency': vendor.order_currency or '',
            'payment_method': vendor.payment_method or '',
            'order_contact': vendor.order_contact or '',
            'order_ext_number': vendor.order_ext_number or '',
            'order_gst_number': vendor.order_gst_number or '',
            'order_language': vendor.order_language or '',
            'order_specify': vendor.order_specify or '',
            'usa_bank_aba': vendor.usa_bank_aba or '',
            'usa_bank_swift_code': vendor.usa_bank_swift_code or '',
            'email_for_payment': vendor.email_for_payment or '',
            'vendor_date': vendor.vendor_date or '',
            'usa_bank_name': vendor.usa_bank_name or '',
            'usa_account_number': vendor.usa_account_number or '',
            'vendor_completed_by': vendor.vendor_completed_by or '',
        })

    @http.route('/submit_customer_form', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def submit_customer_form(self, **post):
        token = post.get('token')

        if not token:
            return request.not_found()

        existing_partner = request.env['res.partner'].sudo().search([('token', '=', token)], limit=1)

        if existing_partner:
            existing_partner.write({
                'street': post.get('street'),
                'street2': post.get('street2'),
                'city': post.get('city'),
                'state_id': request.env['res.country.state'].search([('name', '=', post.get('state'))],
                                                                    limit=1).id if post.get('state') else False,
                'country_id': request.env['res.country'].search([('name', '=', post.get('country'))],
                                                                limit=1).id if post.get('country') else False,
                'phone': post.get('phone_number'),
                'gst_hst_number': post.get('vat_number'),
                'website': post.get('company_website'),
                'date': post.get('business_start_date'),
                'registration_number': post.get('registration_number'),
                'country_parent_company': post.get('country_parent_company'),
                'type_of_business': post.get('type_of_business'),
                'annual_sales': post.get('annual_sales'),
                'place_of_corporation': post.get('place_incorporation'),
                'parent_company': post.get('parent_company'),
                'years_under_current_ownership': post.get('years_ownership'),
                'number_of_location': post.get('number_locations'),
                'fiscal_years_end_date': post.get('fiscal_year_end'),
                'email_for_invoice': post.get('preferred_email_for_invoice'),
                'partner_completed_by': post.get('partner_completed_by'),
                'designation': post.get('designation'),
                'digital_sign_date': post.get('digital_sign_date'),
                'trade_currency': post.get('trade_currency'),
                'state': 'waiting_for_approval',
                'partner_kyc_data_filled': True,
            })

            # Process bank account details
            bank_name = post.get('name_of_bank')
            account_number = post.get('account_number')

            if bank_name or account_number:
                # Search for the bank by name
                bank = request.env['res.bank'].sudo().search([('name', '=', bank_name)], limit=1)

                # If the bank does not exist, create a new one
                if not bank:
                    bank = request.env['res.bank'].sudo().create({
                        'name': bank_name
                    })

                # Search for existing bank account for the partner
                bank_account = request.env['res.partner.bank'].sudo().search([
                    ('bank_name', '=', bank_name),
                    ('acc_number', '=', account_number),
                    ('partner_id', '=', existing_partner.id)
                ], limit=1)

                if not bank_account:
                    # Create a new bank account record
                    request.env['res.partner.bank'].sudo().create({
                        'partner_id': existing_partner.id,
                        'bank_id': bank.id,
                        'acc_number': account_number
                    })
                else:
                    bank_account.write({
                        'acc_number': account_number
                    })

            return "Thank you for submitting details!"
        else:
            return request.not_found()

    @http.route('/submit_vendor_form', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def submit_vendor_form(self, **post):
        token = post.get('token')

        if not token:
            return request.not_found()

        existing_partner = request.env['res.partner'].sudo().search([('token', '=', token)], limit=1)

        if existing_partner:
            existing_partner.write({
                'street': post.get('street'),
                'street2': post.get('street2'),
                'city': post.get('city'),
                'state_id': request.env['res.country.state'].search([('name', '=', post.get('state'))],
                                                                    limit=1).id if post.get('state') else False,
                'country_id': request.env['res.country'].search([('name', '=', post.get('country'))],
                                                                limit=1).id if post.get('country') else False,
                'zip': post.get('postal_code'),
                'phone': post.get('phone_number'),
                'ext_number': post.get('ext_number'),
                'vendor_po_box': post.get('vendor_po_box'),
                'vendor_fax': post.get('vendor_fax'),
                'email_for_order': post.get('email_for_order'),
                'order_template_number': post.get('order_template_number'),
                'quebec_tax_number': post.get('quebec_tax_number'),
                'irs_number': post.get('irs_number'),
                'order_currency': post.get('order_currency'),
                'payment_method': post.get('payment_method'),
                'order_contact': post.get('order_contact'),
                'order_ext_number': post.get('order_ext_number'),
                'order_gst_number': post.get('order_gst_number'),
                'order_language': post.get('order_language'),
                'order_specify': post.get('order_specify'),
                'usa_bank_aba': post.get('usa_bank_aba'),
                'usa_bank_swift_code': post.get('usa_bank_swift_code'),
                'email_for_payment': post.get('email_for_payment'),
                'vendor_date': post.get('vendor_date'),
                'usa_bank_name': post.get('usa_bank_name'),
                'usa_account_number': post.get('usa_account_number'),
                'vendor_completed_by': post.get('vendor_completed_by'),
                'state': 'waiting_for_approval',
                'supplier_kyc_data_filled': True,
            })

            # Process bank account details
            bank_name = post.get('name_of_bank')
            account_number = post.get('account_number')

            if bank_name or account_number:
                # Search for the bank by name
                bank = request.env['res.bank'].sudo().search([('name', '=', bank_name)], limit=1)

                # If the bank does not exist, create a new one
                if not bank:
                    bank = request.env['res.bank'].sudo().create({
                        'name': bank_name
                    })

                # Search for existing bank account for the partner
                bank_account = request.env['res.partner.bank'].sudo().search([
                    ('bank_name', '=', bank_name),
                    ('acc_number', '=', account_number),
                    ('partner_id', '=', existing_partner.id)
                ], limit=1)

                if not bank_account:
                    # Create a new bank account record
                    request.env['res.partner.bank'].sudo().create({
                        'partner_id': existing_partner.id,
                        'bank_id': bank.id,
                        'acc_number': account_number
                    })
                else:
                    bank_account.write({
                        'acc_number': account_number
                    })

            return "Thank you for submitting details!"
        else:
            return request.not_found()
