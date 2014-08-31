// example.js - usage of Cranium MVC


var todo1 = new Cranium.Model({
  title: "",
  completed: ""
});


console.log("First todo title - nothing set: " + todo1.get('title'));

todo1.set({title: "Do something"});


// View instance


var todoView = new Cranium.View({
  // Dom element selector
  el: '#todo',
  // Todo template; underscore templating used
  template: _.template($('.todo-template').innerHTML),
  init: function(model) {
    this.render(model.toJSON());
    this.on(model.id + 'update', this.render.bind(this));
  },
  render: function (data) {
    console.log("View about to render");
    $(this.el).innerHTML = this.template(data);
  },
});


var todoController = new Cranium.Controller({
  // Specify the model to update
  model: todo1,
  // and the view to observe this model
  view: todoView,
  events: {
    '#todo.click': "toggleComplete"
  },

  // Initialize everything
  initialize: function () {
    this.view.init(this.model);
    return this;
  },

  // Toggles the value of the todo in the Model
  toggelComplete: function () {
    var completed = todoController.model.get('completed');
    console.log('todo old "completed" value?', completed);
    todoController.model.set({completed: (!completed) ? 'checked': ''});
    console.log('Todo new "completed" value?', todoController.model.get('completed'));
    return this;
  },
});


// Let's kick start things off
todoController.initialize();
todo1.set({title: "Due to this change Model will notify View and it will re-render"});