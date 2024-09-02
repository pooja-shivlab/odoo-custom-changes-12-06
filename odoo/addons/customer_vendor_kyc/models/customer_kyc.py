from odoo import models, fields, api
import uuid
from odoo.http import request
from odoo.exceptions import UserError
from datetime import timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_for_approval', 'Waiting for Approval'),
        ('publish', 'Publish'),
        ('cancel', 'Cancel'),
    ], string='Status', default='draft')

    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('both', 'Both'),
    ], string='Partner Type', default='customer')
    gst_hst_number = fields.Char(string='GST/HST number')

    # Partner details
    email_for_invoice = fields.Char(string='Preferred Email For Invoice')
    date = fields.Date(string='Business Start Date')
    # business_street_name = fields.Char(string='Street')
    # additional_business_street_name = fields.Char(string='Street 2')
    # business_city = fields.Char(string='City')
    registration_number = fields.Char(string='Registration Number')
    country_parent_company = fields.Char(string='Country of Parent Company')
    type_of_business = fields.Char(string='Type of Business')
    annual_sales = fields.Char(string='Annual Sales')
    place_of_corporation = fields.Char(string='Place of Incorporation or Registration')
    parent_company = fields.Char(string='Parent Company / Group')
    years_under_current_ownership = fields.Integer(string='Years Under Current Ownership')
    number_of_location = fields.Integer(string='Number of Location')
    fiscal_years_end_date = fields.Date(string='Fiscal Years End Date')
    payment_terms = fields.Char(string='Partner Payment Terms')
    requested_credit_limit = fields.Float(string='Requested Credit Limit')
    trade_currency = fields.Selection([
        ('gbp', 'GBP'),
        ('eur', 'EUR'),
        ('usd', 'USD'),
    ], string='Trade Currency')
    partner_completed_by = fields.Char(string='Completed By')
    designation = fields.Char(string='Designation')
    digital_sign_date = fields.Date(string='Date')

    # Supplier details
    ext_number = fields.Char(string='EXT Number')
    vendor_po_box = fields.Char(string='Vendor P.O. Box')
    vendor_fax = fields.Char(string='Vendor Fax')
    email_for_order = fields.Char(string='Email Address for Order Management')
    order_template_number = fields.Char(string='Order Telephone Number')
    quebec_tax_number = fields.Char(string='Order Quebec Tax Number')
    irs_number = fields.Char(string='Order IRS Number')
    order_currency = fields.Selection([
        ('cad', 'CAD'),
        ('eur', 'EUR'),
        ('usd', 'USD'),
    ], string='Order Currency')
    payment_method = fields.Selection([
        ('cheque', 'Cheque'),
        ('direct_deposit', 'Direct Deposit or ACH Payment'),
        ('wire_transfer', 'Wire Transfer'),
    ], string='Order Payment Method')
    order_contact = fields.Char(string='Order Contact')
    order_ext_number = fields.Char(string='Order EXT Number')
    order_gst_number = fields.Char(string='Order GST Number')
    order_language = fields.Selection([
        ('english', 'English'),
        ('french', 'French'),
    ], string='Order Language')
    order_specify = fields.Char(string='Order Specify')
    usa_bank_aba = fields.Char(string='USA Bank ABA Numer')
    usa_bank_swift_code = fields.Char(string='USA Bank Swift Code')
    email_for_payment = fields.Char(string='Email Address for Payment Confirmation')
    vendor_date = fields.Date(string='Vendor Date 1')
    usa_bank_name = fields.Char(string='USA Bank Name')
    usa_account_number = fields.Char(string='USA Account Number')
    vendor_completed_by = fields.Char(string='Vendor Completed By')
    token = fields.Char(string='Token', readonly=True)
    is_send_for_partner_kyc = fields.Boolean(string='Is Send for Partner KYC', default=False)
    is_send_for_supplier_kyc = fields.Boolean(string='Is Send for Supplier KYC', default=False)
    partner_request_url = fields.Char(string='Partner Form URL', readonly=True)
    vendor_request_url = fields.Char(string='Vendor Form URL', readonly=True)
    partner_kyc_data_filled = fields.Boolean(string='Customer Kyc data filled', default=False)
    supplier_kyc_data_filled = fields.Boolean(string='Vendor Kyc data filled', default=False)
    partner_published = fields.Boolean(string='Customer Kyc Done', default=False)
    supplier_published = fields.Boolean(string='Vendor Kyc Done', default=False)

    # KYC reminder and token expiry date-time fields
    form_submit_datetime = fields.Datetime(
        string="Form Submit DateTime",
        readonly=True,
    )
    kyc_reminder_datetime = fields.Datetime(
        string="KYC Reminder DateTime",
        default=lambda self: self._default_kyc_reminder_datetime(),
    )
    token_expiry_datetime = fields.Datetime(
        string="Token Expiry DateTime",
        default=lambda self: self._default_token_expiry_datetime(),
    )
    def _default_kyc_reminder_datetime(self):
        # Ensure that the form submit datetime is available
        if not self.form_submit_datetime:
            return False

        reminder_interval_number = int(
            self.env['ir.config_parameter'].sudo().get_param('reminder_interval_number', default=0)
        )
        reminder_interval_type = self.env['ir.config_parameter'].sudo().get_param(
            'reminder_interval_type', default='days'
        )
        if reminder_interval_type == 'days':
            delta = timedelta(days=reminder_interval_number)
        else:  # hours
            delta = timedelta(hours=reminder_interval_number)

        return self.form_submit_datetime + delta

    def _default_token_expiry_datetime(self):
        # Ensure that the form submit datetime is available
        if not self.form_submit_datetime:
            return False

        token_expire_interval_number = int(
            self.env['ir.config_parameter'].sudo().get_param('token_expire_interval_number', default=0)
        )
        token_expire_interval_type = self.env['ir.config_parameter'].sudo().get_param(
            'token_expire_interval_type', default='days'
        )
        if token_expire_interval_type == 'days':
            delta = timedelta(days=token_expire_interval_number)
        else:  # hours
            delta = timedelta(hours=token_expire_interval_number)

        return self.form_submit_datetime + delta

    supplier_form_submit_datetime = fields.Datetime(
        string="Supplier Form Submit DateTime",
        readonly=True,
    )
    supplier_kyc_reminder_datetime = fields.Datetime(
        string="Supplier KYC Reminder DateTime",
        default=lambda self: self._default_supplier_kyc_reminder_datetime(),
    )
    supplier_token_expiry_datetime = fields.Datetime(
        string="Supplier Token Expiry DateTime",
        default=lambda self: self._default_supplier_token_expiry_datetime(),
    )
    def _default_supplier_kyc_reminder_datetime(self):
        # Ensure that the form submit datetime is available
        if not self.supplier_form_submit_datetime:
            return False

        reminder_interval_number = int(
            self.env['ir.config_parameter'].sudo().get_param('reminder_interval_number', default=0)
        )
        reminder_interval_type = self.env['ir.config_parameter'].sudo().get_param(
            'reminder_interval_type', default='days'
        )
        if reminder_interval_type == 'days':
            delta = timedelta(days=reminder_interval_number)
        else:  # hours
            delta = timedelta(hours=reminder_interval_number)

        return self.supplier_form_submit_datetime + delta

    def _default_supplier_token_expiry_datetime(self):
        # Ensure that the form submit datetime is available
        if not self.supplier_form_submit_datetime:
            return False

        token_expire_interval_number = int(
            self.env['ir.config_parameter'].sudo().get_param('token_expire_interval_number', default=0)
        )
        token_expire_interval_type = self.env['ir.config_parameter'].sudo().get_param(
            'token_expire_interval_type', default='days'
        )
        if token_expire_interval_type == 'days':
            delta = timedelta(days=token_expire_interval_number)
        else:  # hours
            delta = timedelta(hours=token_expire_interval_number)

        return self.supplier_form_submit_datetime + delta

    @api.model
    def default_get(self, fields_list):
        res = super(ResPartner, self).default_get(fields_list)
        if 'token' in fields_list:
            res['token'] = uuid.uuid4().hex
        return res

    def partner_send_form_action(self):
        for partner in self:
            partner.form_submit_datetime = fields.Datetime.now()
            # Recalculate the reminder and expiry datetimes
            partner.kyc_reminder_datetime = partner._default_kyc_reminder_datetime()
            partner.token_expiry_datetime = partner._default_token_expiry_datetime()

            # Define the URL for the form
            partner.is_send_for_partner_kyc = True
            base_url = '/customer_form/%s' % partner.token
            url = request.httprequest.host_url.rstrip('/') + base_url
            partner.partner_request_url = url

            template = self.env.ref('customer_vendor_kyc.email_template_form').id
            if partner.email:
                self.env['mail.template'].browse(template).send_mail(
                    partner.id, force_send=True,
                    email_values={'email_to': partner.email, 'email_from': 'pooja.ahuja@shivlab.com'})
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'The registration link has been sent to the contact.',
                        'sticky': False,
                    },
                }
            else:
                raise UserError("Email is required!")

    def supplier_send_form_action(self):
        for partner in self:
            partner.supplier_form_submit_datetime = fields.Datetime.now()
            # Recalculate the reminder and expiry datetimes
            partner.supplier_kyc_reminder_datetime = partner._default_supplier_kyc_reminder_datetime()
            partner.supplier_token_expiry_datetime = partner._default_supplier_token_expiry_datetime()

            # Define the URL for the form
            # url = '/customer_form/%s' % partner.id
            partner.is_send_for_supplier_kyc = True
            base_url = '/vendor_form/%s' % partner.token
            url = request.httprequest.host_url.rstrip('/') + base_url
            partner.vendor_request_url = url

            template = self.env.ref('customer_vendor_kyc.email_template_form').id
            if partner.email:
                self.env['mail.template'].browse(template).send_mail(
                    partner.id, force_send=True,
                    email_values={'email_to': partner.email, 'email_from': 'pooja.ahuja@shivlab.com'})
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'The registration link has been sent to the contact.',
                        'sticky': False,
                    },
                }
            else:
                raise UserError("Email is required!")

    def publish_partner(self):
        for record in self:
            if record.state == 'waiting_for_approval':
                record.state = 'publish'
                if record.partner_type in ['customer', 'both']:
                    record.partner_published = True
                if record.partner_type in ['supplier', 'both']:
                    record.supplier_published = True

    def decline_partner(self):
        for record in self:
            if record.state == 'waiting_for_approval':
                record.state = 'cancel'
                if record.partner_type in ['customer', 'both']:
                    record.partner_published = False
                if record.partner_type in ['supplier', 'both']:
                    record.supplier_published = False
