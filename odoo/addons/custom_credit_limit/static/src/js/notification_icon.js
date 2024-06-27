/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class CustomNotificationIcon extends Component {
    static template = "custom_credit_limit.assets";

    setup() {
        this.state = useState({
            isOpen: false,
        });

        // Toggle dropdown visibility
        this.toggleDropdown = () => {
            this.state.isOpen = !this.state.isOpen;
        };
    }
}

registry
    .category("systray")
    .add("custom.notification_icon", { Component: CustomNotificationIcon }, { sequence: 20 });
