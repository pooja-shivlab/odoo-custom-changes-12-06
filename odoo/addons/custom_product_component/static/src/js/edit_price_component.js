/** @odoo-module **/

import { booleanToggleField, BooleanToggleField } from '@web/views/fields/boolean_toggle/boolean_toggle_field';
import { registry } from '@web/core/registry';
import { useRef, useEffect, useState } from '@odoo/owl';

export class CustomBooleanToggle extends BooleanToggleField {
    setup() {
        super.setup(); // Call super.setup() to initialize from BooleanToggleField
        this.state = useState({ checked: this.props.value });
    }

    async onChange(newValue) {
        this.state.checked = newValue;
        console.log("00000000000000000000000000000000000", this.state.checked);
        this.togglePriceFieldEditable();
    }

    async togglePriceFieldEditable() {
        // Manipulate DOM based on component state
        const formView = document.querySelector('.o_component_form_view');
        if (formView) {
            const priceField = formView.querySelector('.o_field_widget[name="price"]');
            if (priceField) {
                if (this.state.checked) {
                    console.log("======================");
//                    priceField.classList.remove('o_readonly');
                    priceField.removeAttribute('readonly'); // Enable editing
                } else {
                    console.log("-----------------------");
//                    priceField.classList.add('o_readonly');
                    priceField.setAttribute('readonly', true); // Disable editing
                }
            }
        }
    }
}

// Define your component configuration
export const customBooleanToggle = {
    ...booleanToggleField, // Assuming booleanToggleField is defined elsewhere
    component: CustomBooleanToggle, // Use your custom component class
};

// Register your custom component
registry.category('fields').add('custom_boolean_toggle', customBooleanToggle);

export default CustomBooleanToggle; // Export if needed elsewhere
