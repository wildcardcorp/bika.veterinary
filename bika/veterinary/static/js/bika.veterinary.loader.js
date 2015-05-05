'use strict';
window.bika = window.bika || { lims: {} };
window.bika['veterinary']={};
window.jarn.i18n.loadCatalog("bika.veterinary");
var _s = window.jarn.i18n.MessageFactory("bika.veterinary");

/**
 * Dictionary of JS objects to be loaded at runtime.
 * The key is the DOM element to look for in the current page. The
 * values are the JS objects to be loaded if a match is found in the
 * page for the specified key. The loader initializes the JS objects
 * following the order of the dictionary.
 */
window.bika.veterinary.controllers =  {

};

window.bika.veterinary.initialized = false;

/**
 * Initializes all bika.veterinary js stuff
 * Add the bika.veterinary controllers inside bikia.lims controllers'
 * dict to be load together.
 */
window.bika.veterinary.initialize = function() {
    if (bika.lims.initialized==true && bika.health.initialized==true) {
        // Using only lims and veterinary because window.bika.lims.controllers was extended on health
        window.bika.lims.controllers = $.extend(window.bika.lims.controllers, window.bika.health.controllers,window.bika.veterinary.controllers);
        // We need to force bika.lims.loader to load the bika.veterinary controllers.
        return window.bika.lims.initview();
    }
    // We should wait after bika.lims has been initialized.
    setTimeout(function() {
        return window.bika.veterinary.initialize();
    }, 500);
};

(function( $ ) {
$(document).ready(function(){

    // Initializes bika.veterinary.
    var length = window.bika.veterinary.initialize();
    window.bika.veterinary.initialized = true;

});
}(jQuery));

