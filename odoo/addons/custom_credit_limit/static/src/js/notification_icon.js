/* @odoo-module */

import { Component, useState, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { renderToElement } from "@web/core/utils/render";
import { useService } from "@web/core/utils/hooks";

export class CustomNotificationIcon extends Component {
    static template = "custom_credit_limit.assets";

    setup() {
        this.state = useState({
            isOpen: false,
            warning: '',
            type: '',
            customer: '',
            count : 0,
        });

        // Bind the methods
        this.handleWarningClick = this.handleWarningClick.bind(this);
        this.handleExternalClick = this.handleExternalClick.bind(this);
        useExternalListener(window, "click", this.handleExternalClick, { capture: true });

        // Toggle dropdown visibility
        this.toggleDropdown = () => {
            this.state.isOpen = !this.state.isOpen;
            if (this.state.isOpen  && this.state.type) {
                this.fetchCustomerId();
                this.fetchWarnings(this.state.type, this.state.customer);
            }
        };

        // Add event listener for the "Stay here" button
        this.stayHere = () => {
            $('#my_modal').modal('hide');  // Close the modal
        };

        this.discardChanges = () => {
            $('#my_modal').modal('hide');  // Close the modal first
            this.env.services.action.doAction('custom_credit_limit.partner_overview');
        };
    }


    async fetchCustomerId() {
        const customerIdElement = document.querySelector('.o_field_widget[name="partner_id"] input');
        if (customerIdElement) {
        // Extract the value or data-id (depending on how Odoo renders it)
            const customerId = customerIdElement.value || customerIdElement.dataset.id;
            this.state.customer = customerId;
        }
    }

    async fetchWarnings(type, customer) {
        try {
            console.log("=====================================", type, customer);

            const response = await fetch('/web/dataset/call_kw/sale.order/get_credit_limit_warnings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ type: type, customer: customer })
            });

            const data = await response.json();
            console.log('Fetched data:', data);

            if (data.result && data.result.result.message) {
                this.state.warning = data.result.result.message;
                this.state.count = data.result.result.count;

                  if (type === 'soft') {
                        this.state.count = 0;
                  } else if (type === 'hard') {
                        this.state.count =  this.state.count;
                  }

                  if (type === 'soft' || type === 'hard') {
                    // Check if the modal already exists
                    let modalElement = document.getElementById('my_modal');
                    if (modalElement) {
                        // Update the modal content
                        modalElement.querySelector('.modal-body p').textContent = this.state.warning;
                    } else {
                        // Create and append a new modal
                        modalElement = renderToElement('my_modal_relay', { warning: this.state.warning });
                        $(document.body).append(modalElement);
                    }

                    // Show the modal
                    $('#my_modal').modal('show');

                    // Attach event listeners to the buttons
                    document.getElementById('stay-here-btn').addEventListener('click', this.stayHere);
                    document.getElementById('discard-changes-btn').addEventListener('click', this.discardChanges);
                    }
                }else{
                    this.env.services.action.doAction('custom_credit_limit.partner_overview');
                }
        } catch (error) {
            console.error('Error fetching warning:', error);
        }
    }

    handleWarningClick(type) {
        this.state.type = type;
        this.toggleDropdown();
    }

    // Dropdown close while clicking on any other thing is page
    handleExternalClick(event) {
        Object.assign(this.state, { isOpen: false, type: '', customer: '', warning: '' });
    }
}

registry
    .category("systray")
    .add("custom.notification_icon", { Component: CustomNotificationIcon }, { sequence: 20 });
