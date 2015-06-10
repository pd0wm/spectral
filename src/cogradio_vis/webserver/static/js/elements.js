/**
 * Classes defining the behaviour of the various control elements available.
 */

/* Base class */
 var Element = function(id, key) {
    this.id = id;
    this.key = key;
    Control.register(id, this);
 }

/* Text element initialisation and update logic */
var TextElement = function(id, key) {
    this.element = $("#" + id);

    Element.call(this, id, key);
};

TextElement.prototype = Object.create(Element.prototype);

TextElement.prototype.update = function(value) {
    this.element.html(value)
};

/* Slider initialisation and update logic */
var SliderElement = function(id, key) {
    this.slider = $("#" + id).slider();

    var that = this;
    this.slider.on('change', function(e) {
        Control.update(that, e.value.newValue);
    });

    Element.call(this, id, key);
};

SliderElement.prototype = Object.create(Element.prototype);

SliderElement.prototype.update = function(value) {
    this.slider.slider('setValue', value);
};

/* Checkbox initialisation and update logic */
var CheckboxElement = function(id, key) {
    this.checkbox = $("#" + id);

    $('#' + id).on('change', function(ev) {
        Control.update(this, this.checked);
    });

    Element.call(this, id, key);
};

CheckboxElement.prototype = Object.create(Element.prototype);

CheckboxElement.prototype.update = function(value) {
    this.checkbox.prop('checked', value);
};

/* Visualisation initialisation and update logic */
var VisualisationElement = function(id, key) {
    Visualisation.init(id);
    this.container = $("#" + id);

    this.container.on("change", ".visualisation-data", function() {
        Visualisation.init(id);
    });
    this.container.on("change", ".visualisation-type", function() {
        Visualisation.init(id);
    });

    Element.call(this, id, key);
}

VisualisationElement.prototype = Object.create(Element.prototype);

/* Sweep initialisation and update logic */
var SweepElement = function(id, key) {
    Visualisation.init(id);
    this.container = $("#" + id);

    this.container.on("change", ".visualisation-data", function() {
        Visualisation.init(id);
    });

    Element.call(this, id, key);
}

SweepElement.prototype = Object.create(Element.prototype);
