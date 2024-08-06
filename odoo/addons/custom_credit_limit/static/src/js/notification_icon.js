/* @odoo-module */

import { Component, useState, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useDiscussSystray } from "@mail/utils/common/hooks";

export class CustomNotificationIcon extends Component {
    static template = "custom_credit_limit.assets";

    setup() {
        this.state = useState({
            isOpen: false,
            warning: {}
        });
        useExternalListener(window, "click", this.handleExternalClick, { capture: true });

        // Toggle dropdown visibility
        this.toggleDropdown = () => {
            this.state.isOpen = !this.state.isOpen;
            if (this.state.isOpen) {
               this.fetchWarnings();  // Fetch warnings when opening dropdown
            }
        };
    }

    async fetchWarnings() {
        try {
            const response = await fetch('/web/dataset/call_kw/sale.order/get_credit_limit_warnings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            const data = await response.json();
            console.log('Fetched data:', data);

            if (data.result) {
                this.state.warning = data.result.result.message;
            } else {
                console.error('Unexpected data format', data);
            }
        } catch (error) {
            console.error('Error fetching warning:', error);
        }
    }



    // Dropdown close while clicking on any other thing is page
    handleExternalClick(event) {
        Object.assign(this.state, { isOpen: false });
    }
}

registry
    .category("systray")
    .add("custom.notification_icon", { Component: CustomNotificationIcon }, { sequence: 20 });
