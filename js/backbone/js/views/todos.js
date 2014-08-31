// js/views/todos.js


var app = app || {};


// Todo Item View
// ---------------


// The DOm element for a todo item...
app.TodoView = Backbone.View.extend({
  tagName: 'li',
  // Cache the template function for a single item.

  template: _.template($("#item-template").html()),

  // The DOM events specific to an item.
  events: {
    'dbclick label': 'edit',
    'keypress .edit': 'updateOnEnter',
    'blur .edit': 'close',
    'click .toggle': 'togglecompleted',
    'click .destory': 'clear'
  },

  initialize: function() {
    this.listenTo(this.model, 'change', this.render);
    this.listenTo(this.model, 'destory', this.remove);
    this.listenTo(this.model, 'visible', this.toggleVisible);
  },

  // Re-renders the titles of the todo item.
  render: function() {
    this.$el.html(this.template(this.model.toJSON()));
    this.$input = this.$('.edit');

    this.$el.toggleClass('completed', this.model.get('completed'));
    this.toggleVisible();
    return this;
  },

  // Toggles visibility of item
  toggleVisible: function() {
    this.$el.toggleClass('hidden', this.isHidden());
  },

  isHidden: function() {
    var isCompleted = this.model.get('completed');
    return ( // hidden cases only
      (!isCompleted && app.TodoFilter === 'completed')
      || (isCompleted && app.TodoFilter === 'active')
    );
  },

  togglecompleted: function () {
    this.model.toggle();
  },

  // Switch this view into `"editing"` mode, displaying the input field.
  edit: function() {
    this.$el.addClass('editing');
    this.$input.focus();
  },

  // Close the `"editing"` mode, saving changes to the todo.
  close: function() {
    var value = this.$input.val().trim();

    if (value) {
      this.model.save({title: value});
    }
    this.$el.removeClass('editing');
  },

  clear: function() {
    this.model.destory();
  },

  // checks that the user has hit the return/enter key and executes close() function
  updateOnEnter: function(e) {
    if (e.which === ENTER_KEY) {
      this.close();
    }
  }

});
