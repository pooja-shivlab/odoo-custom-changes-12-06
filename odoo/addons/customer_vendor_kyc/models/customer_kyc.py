from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_for_approval', 'Waiting for Approval'),
        ('publish', 'Publish'),
    ], string='Status', default='draft')

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
