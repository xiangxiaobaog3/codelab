var app = app || {};


// Todo collection
// ---------------

// The collection of todos is backed by *localStorage* instead of a remote
// server


var TodoList = Backbone.Collection.extend({

  // Reference to this collection's model.
  model: app.Todo,

  // Save all of the todo items under the `"todos-backbone"` namespace.
  localStorage: new Backbone.LocalStorage('todos-backbone'),

  // Filter down the list to only todo items that are still not finished.
  remaining: function() {
    return this.without.apply(this, this.completed());
    // use filter instead of without
    return this.filter(function(todo) {
      return !todo.get('completed');
    });
  },

  completed: function () {
    return this.filter(function(todo) {
      return todo.get('completed');
    });
  },

  // We keep the Todos in sequential order, despite being saved by unordered
  // GUID in the database. This generates the next order number for new items.
  nextOrder: function () {
    if (!this.length) {
      return 1;
    }
    return this.last().get('order') + 1;
  },

  // Todos are sorted by their original insertion order.
  comparator: function (todo) {
    return todo.get('order');
  }

});


app.Todos = new TodoList();