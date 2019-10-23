import { r as registerInstance, B as Build } from './core-950489bb.js';
import { c as createOverlay, d as dismissOverlay, g as getOverlay } from './overlays-a2b1b53e.js';

const ModalController = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        if (Build.isDev) {
            console.warn(`[DEPRECATED][ion-modal-controller] Use the modalController export from @ionic/core:
  import { modalController } from '@ionic/core';
  const modal = await modalController.create({...});`);
        }
    }
    /**
     * Create a modal overlay with modal options.
     *
     * @param options The options to use to create the modal.
     */
    create(options) {
        return createOverlay('ion-modal', options);
    }
    /**
     * Dismiss the open modal overlay.
     *
     * @param data Any data to emit in the dismiss events.
     * @param role The role of the element that is dismissing the modal.
     * This can be useful in a button handler for determining which button was
     * clicked to dismiss the modal.
     * Some examples include: ``"cancel"`, `"destructive"`, "selected"`, and `"backdrop"`.
     * @param id The id of the modal to dismiss. If an id is not provided, it will dismiss the most recently opened modal.
     */
    dismiss(data, role, id) {
        return dismissOverlay(document, data, role, 'ion-modal', id);
    }
    /**
     * Get the most recently opened modal overlay.
     */
    async getTop() {
        return getOverlay(document, 'ion-modal');
    }
};

export { ModalController as ion_modal_controller };
