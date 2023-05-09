document.getElementById('todo-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var todoInput = document.getElementById('todo-input');
    var todoText = todoInput.value.trim();
    if (todoText !== '') {
      addTodoItem(todoText);
      todoInput.value = '';
    }
  });
  
  function addTodoItem(todoText) {
    var todoList = document.getElementById('todo-list');
    var li = document.createElement('li');
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    var label = document.createElement('label');
    label.textContent = todoText;
    li.appendChild(checkbox);
    li.appendChild(label);
    todoList.appendChild(li);
  }
  