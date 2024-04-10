

    const { Dialog } = require("@web/core/dialog/dialog");
    const { registry } = require("@web/core/registry");
    console.log(registry)
    const { useService } = require("@web/core/utils/hooks");

    const { Component, useState, onWillStart } = owl;
    console.log(Component)

    // Define the To-Do List component
 class TodoList extends Component {
        setup() {
            // Initialize state for tasks
            this.state = useState({
                tasks: [],
                newTask: '',
            });
        }

        // Method to add a new task
        addTask() {
            const { tasks, newTask } = this.state;
            if (newTask.trim() !== '') {
                this.state.tasks = [...tasks, { text: newTask, completed: false }];
                this.state.newTask = ''; // Clear the input field
            }
        }

        // Method to mark a task as completed
        toggleTask(index) {
            this.state.tasks[index].completed = !this.state.tasks[index].completed;
        }

        // Method to remove a task
        removeTask(index) {
            this.state.tasks.splice(index, 1);
        }
    }

    // Register the To-Do List component
    TodoList.template = 'todo.TodoList';
