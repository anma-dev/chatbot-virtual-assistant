import { r as registerInstance, B as Build } from './core-950489bb.js';
import { c as createOverlay, d as dismissOverlay, g as getOverlay } from './overlays-a2b1b53e.js';

const PopoverController = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        if (Build.isDev) {
            console.warn(`[DEPRECATED][ion-popover-controller] Use the popoverController export from @ionic/core:
  import { popoverController } from '@ionic/core';
  const popover = await popoverController.create({...});`);
        }
    }
    /**
     * Create a popover overlay with popover options.
     *
     * @param options The options to use to create the popover.
     */
    create(options) {
        return createOverlay('ion-popover', options);
    }
    /**
     * Dismiss the open popover overlay.
     *
     * @param data Any data to emit in the dismiss events.
     * @param role The role of the element that is dismissing the popover.
     * This can be useful in a button handler for determining which button was
     * clicked to dismiss the popover.
     * Some examples include: ``"cancel"`, `"destructive"`, "selected"`, and `"backdrop"`.
     * @param id The id of the popover to dismiss. If an id is not provided, it will dismiss the most recently opened popover.
     */
    dismiss(data, role, id) {
        return dismissOverlay(document, data, role, 'ion-popover', id);
    }
    /**
     * Get the most recently opened popover overlay.
     */
    async getTop() {
        return getOverlay(document, 'ion-popover');
    }
};

export { PopoverController as ion_popover_controller };
