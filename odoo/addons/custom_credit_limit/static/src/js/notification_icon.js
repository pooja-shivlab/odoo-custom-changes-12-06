/* @odoo-module */

import { Component, useState, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useDiscussSystray } from "@mail/utils/common/hooks";

export class CustomNotificationIcon extends Component {
    static template = "custom_credit_limit.assets";

    setup() {
        this.state = useState({
            isOpen: false,
        });

        useExternalListener(window, "click", this.handleExternalClick, { capture: true });

        // Toggle dropdown visibility
        this.toggleDropdown = () => {
            this.state.isOpen = !this.state.isOpen;
        };
    }

    // Dropdown close while clicking on any other thing is page
    handleExternalClick(event) {
        Object.assign(this.state, { isOpen: false });
    }
}

registry
    .category("systray")
    .add("custom.notification_icon", { Component: CustomNotificationIcon }, { sequence: 20 });
