const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const taskForm = document.getElementById('taskForm');
const editTaskForm = document.getElementById('editTaskForm');
const tasksContainer = document.getElementById('tasksContainer');
const editModal = document.getElementById('editModal');
const closeModal = document.querySelector('.close');

// Event Listeners
document.addEventListener('DOMContentLoaded', loadTasks);
taskForm.addEventListener('submit', handleAddTask);
editTaskForm.addEventListener('submit', handleEditTask);
closeModal.addEventListener('click', closeEditModal);
window.addEventListener('click', (e) => {
    if (e.target === editModal) {
        closeEditModal();
    }
});

// Load all tasks
async function loadTasks() {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/tasks`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Error loading tasks:', error);
        showError('Failed to load tasks. Make sure the backend server is running.');
    }
}

// Display tasks in the UI
function displayTasks(tasks) {
    if (tasks.length === 0) {
        tasksContainer.innerHTML = '<p class="loading">No tasks found. Add your first task!</p>';
        return;
    }

    tasksContainer.innerHTML = tasks.map(task => `
        <div class="task-card">
            <div class="task-header">
                <h3 class="task-title">${escapeHtml(task.title)}</h3>
                <span class="task-status status-${task.status}">${task.status}</span>
            </div>
            <p class="task-description">${escapeHtml(task.description)}</p>
            <div class="task-actions">
                <button class="btn-edit" onclick="openEditModal(${task.id})">Edit</button>
                <button class="btn-delete" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Handle add task form submission
async function handleAddTask(e) {
    e.preventDefault();
    
    const formData = new FormData(taskForm);
    const taskData = {
        title: formData.get('title'),
        description: formData.get('description'),
        status: formData.get('status')
    };

    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const newTask = await response.json();
        showSuccess('Task added successfully!');
        taskForm.reset();
        loadTasks();
    } catch (error) {
        console.error('Error adding task:', error);
        showError('Failed to add task. Please try again.');
    }
}

// Open edit modal
async function openEditModal(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const task = await response.json();
        
        document.getElementById('editTaskId').value = task.id;
        document.getElementById('editTitle').value = task.title;
        document.getElementById('editDescription').value = task.description;
        document.getElementById('editStatus').value = task.status;
        
        editModal.style.display = 'block';
    } catch (error) {
        console.error('Error loading task for edit:', error);
        showError('Failed to load task details.');
    }
}

// Handle edit task form submission
async function handleEditTask(e) {
    e.preventDefault();
    
    const taskId = document.getElementById('editTaskId').value;
    const formData = new FormData(editTaskForm);
    const taskData = {
        title: formData.get('title'),
        description: formData.get('description'),
        status: formData.get('status')
    };

    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const updatedTask = await response.json();
        showSuccess('Task updated successfully!');
        closeEditModal();
        loadTasks();
    } catch (error) {
        console.error('Error updating task:', error);
        showError('Failed to update task. Please try again.');
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        showSuccess('Task deleted successfully!');
        loadTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
        showError('Failed to delete task. Please try again.');
    }
}

// Close edit modal
function closeEditModal() {
    editModal.style.display = 'none';
}

// Utility functions
function showLoading() {
    tasksContainer.innerHTML = '<p class="loading">Loading tasks...</p>';
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    
    // Remove existing error messages
    const existingError = document.querySelector('.error');
    if (existingError) {
        existingError.remove();
    }
    
    document.querySelector('.container').insertBefore(errorDiv, document.querySelector('main'));
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success';
    successDiv.textContent = message;
    
    // Remove existing success messages
    const existingSuccess = document.querySelector('.success');
    if (existingSuccess) {
        existingSuccess.remove();
    }
    
    document.querySelector('.container').insertBefore(successDiv, document.querySelector('main'));
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}