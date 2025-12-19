/**
 * Handles client-side logic for interacting with the API endpoints,
 * updating the UI, and managing local storage.
 */

const API_BASE_URL = ''; // You can set a base URL here if needed, e.g., '/api'

/**
 * Fetches all tasks from the server and updates the UI.
 */
async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/get_tasks`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const tasks = await response.json();
        updateUI(tasks);
    } catch (error) {
        console.error("Failed to fetch tasks:", error);
        displayError("Failed to fetch tasks. Please try again.");
    }
}

/**
 * Adds a new task to the server and updates the UI.
 * @param {string} text - The text of the new task.
 */
async function addTask(text) {
    try {
        const response = await fetch(`${API_BASE_URL}/add_task`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const tasks = await response.json();
        updateUI(tasks);
    } catch (error) {
        console.error("Failed to add task:", error);
        displayError("Failed to add task. Please try again.");
    }
}

/**
 * Deletes a task from the server and updates the UI.
 * @param {string} id - The ID of the task to delete.
 */
async function deleteTask(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/delete_task/${id}`, {
            method: 'POST',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const tasks = await response.json();
        updateUI(tasks);
    } catch (error) {
        console.error("Failed to delete task:", error);
        displayError("Failed to delete task. Please try again.");
    }
}

/**
 * Completes a task on the server and updates the UI.
 * @param {string} id - The ID of the task to complete.
 */
async function completeTask(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/complete_task/${id}`, {
            method: 'POST',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const tasks = await response.json();
        updateUI(tasks);
    } catch (error) {
        console.error("Failed to complete task:", error);
        displayError("Failed to complete task. Please try again.");
    }
}

/**
 * Updates the UI with the given tasks.
 * @param {Array<Object>} tasks - An array of task objects.
 */
function updateUI(tasks) {
    const todoList = document.getElementById('todo-list');
    if (!todoList) {
        console.error("Todo list element not found.");
        return;
    }

    // Clear existing list
    todoList.innerHTML = '';

    tasks.forEach(task => {
        const listItem = document.createElement('li');
        listItem.className = 'todo-item';
        listItem.innerHTML = `
            <input type="checkbox" id="task-${task.id}" ${task.completed ? 'checked' : ''}>
            <label for="task-${task.id}" class="${task.completed ? 'completed' : ''}">${task.text}</label>
            <button class="delete-button" data-id="${task.id}">Delete</button>
        `;
        todoList.appendChild(listItem);

        // Add event listeners for complete and delete
        const checkbox = listItem.querySelector('input[type="checkbox"]');
        checkbox.addEventListener('change', () => completeTask(task.id));

        const deleteButton = listItem.querySelector('.delete-button');
        deleteButton.addEventListener('click', () => deleteTask(task.id));
    });
}

/**
 * Displays an error message to the user.
 * @param {string} message - The error message to display.
 */
function displayError(message) {
    const errorDiv = document.getElementById('error-message');
    if (!errorDiv) {
        console.error("Error message element not found.");
        return;
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block'; // Make sure the error message is visible
}

/**
 * Hides the error message.
 */
function hideError() {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}


/**
 * Initializes the application.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Fetch tasks on load
    fetchTasks();

    // Add task form submission
    const addTaskForm = document.getElementById('add-task-form');
    if (!addTaskForm) {
        console.error("Add task form not found.");
        return;
    }

    addTaskForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideError(); // Hide any previous errors

        const taskInput = document.getElementById('task-input');
        if (!taskInput) {
            console.error("Task input not found.");
            return;
        }
        const taskText = taskInput.value.trim();

        if (taskText === '') {
            displayError("Task text cannot be empty.");
            return;
        }

        await addTask(taskText);
        taskInput.value = ''; // Clear the input
    });
});
