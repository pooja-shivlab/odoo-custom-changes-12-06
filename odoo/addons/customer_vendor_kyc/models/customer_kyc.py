from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


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
    email_for_invoice = fields.Char(string='Preferred Email For Invoice')
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
    date = fields.Date(string='Business Start Date')
    name = fields.Char(string='Completed By')
    designation = fields.Char(string='Designation')
    digital_sign_date = fields.Date(string='Date')
    ext_number = fields.Char(string='EXT Number')
    vendor_po_box = fields.Char(string='Vendor P.O. Box')
    vendor_fax = fields.Char(string='Vendor Fax')
    email_for_order = fields.Char(string='Email Address for Order Management')
    order_template_number = fields.Char(string='Order Template Number')
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

    def send_form_action(self):
        for partner in self:
            form = self.env['customer.details.form'].create({
                'customer_id': partner.id,
            })
            _logger.info("Created form: %s", form)
            link = '/customer/form/%s' % (form.token)
            _logger.info("Generated link: %s", link)

            try:
                template = self.env.ref('customer_vendor_kyc.email_template_form')
                if template:
                    # Prepare the context with the link
                    ctx = {
                        'link': link,
                    }
                    _logger.info("Email context: %s", ctx)  # Log the context for debugging
                    # Generate the email content from the template
                    template.with_context(ctx).send_mail(
                        partner.id,
                        force_send=True,
                        email_values={'email_to': partner.email, 'email_from': 'pooja.ahuja@shivlab.com'}
                    )
                    partner.state = 'waiting_for_approval'
            except Exception as e:
                _logger.error("Failed to send email: %s", e)
                raise
