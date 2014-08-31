// cranium.js


// Attributes represents data, model's properties.
// These are to be passed at Modl instantiation.
// Also we are creating id for each Model instance
// so that it can identify itself (e.g on change
// anoucements)

function Cranium () {};

var Model = Cranium.Model = function (attributes) {
  this.id = _.unique('model');
  this.attributes = attributes || {};
};


// Getter (accessor) method;
// returns named data item

Cranium.Model.prototype.get = function (attrName) {
  return this.attributes[attrName];
};

// Setter (mutator) method;
// Set/mix in into model mapped data (e.g. {name: "Jhon"})

Cranium.Model.prototype.set = function (attrs) {
  if (_.isObject(attrs)) {
    _.extend(this.attributes, attrs);
    this.change(this.attributes);
  }
  return this;
};


// Returns clone of the Models data object
// (used for view template rendering)

Cranium.Model.prototype.toJSON = function (options) {
  return _.clone(this.attributes);
};


// Helper function that anoucements changes to the Model
// and passes the new data
Cranium.Model.prototype.change = function (attrs) {
  this.trigger(this.id + 'update', attrs);
};


// Mix in Event system
_.extend(Cranium.Model.prototype, Cranium.Events);


// DOM view
var View = Cranium.View = function (options) {
  // Mix in options object (e.g extending functionality)
  _.extend(this, options);
};


// Mix in Event system
_.extend(Cranium.View.prototype, Cranium.Events);


// Controller tying together a model and view
var Controller = Cranium.Controller = function (options) {
  // Mix in options object (e.g extending functionality)
  _.extend(this, options);
  this.id = _.uniqueId('controller');
  var parts, selectors, eventType;

  // Parse Events object passed during the definition of the
  // controller and maps it to the defined method to handled it;

  if (this.events) {
    _.each(this.events, function(method, eventName) {
      parts = eventName.split('.');
      selectors = parts[0];
      eventType = parts[1];
      $(selector)['on' + eventType] = this[method];
    }.bind(this));
  }
};