from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for tasks
tasks = []
task_counter = 1
lock = threading.Lock()  # Thread safety for concurrent access

class Task:
    def __init__(self, title, description, status="pending"):
        global task_counter
        with lock:
            self.id = task_counter
            task_counter += 1
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(self, title=None, description=None, status=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        self.updated_at = datetime.now().isoformat()

# Initialize with some sample data
def initialize_sample_data():
    sample_tasks = [
    Task("Create Website using Docker", "Develop a distributed parallel system website using Docker", "in-progress"),
    Task("Formal Language & Automata Assignment", "Complete the Formal Language and Automata theory assignment", "pending"),
    Task("Operating System Design Assignment", "Work on the Operating System Design assignment", "pending"),
    Task("Create Portfolio Website", "Design and develop a personal portfolio website", "in-progress"),
    Task("Apply for Internships", "Search and apply for relevant internship opportunities", "in-progress")
]
    
    with lock:
        tasks.extend(sample_tasks)

# Initialize sample data
initialize_sample_data()

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'message': 'Task Manager API is running!',
        'version': '1.0.0',
        'endpoints': {
            'GET /tasks': 'Get all tasks',
            'POST /tasks': 'Create a new task',
            'GET /tasks/<id>': 'Get a specific task',
            'PUT /tasks/<id>': 'Update a specific task',
            'DELETE /tasks/<id>': 'Delete a specific task'
        }
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    with lock:
        return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'title' not in data or 'description' not in data:
            return jsonify({'error': 'Title and description are required'}), 400
        
        # Validate status
        valid_statuses = ['pending', 'in-progress', 'completed']
        status = data.get('status', 'pending')
        if status not in valid_statuses:
            return jsonify({'error': f'Status must be one of: {valid_statuses}'}), 400
        
        # Create new task
        new_task = Task(
            title=data['title'].strip(),
            description=data['description'].strip(),
            status=status
        )
        
        with lock:
            tasks.append(new_task)
        
        return jsonify(new_task.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    with lock:
        task = next((task for task in tasks if task.id == task_id), None)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a specific task"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        with lock:
            task = next((task for task in tasks if task.id == task_id), None)
            
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            
            # Validate status if provided
            if 'status' in data:
                valid_statuses = ['pending', 'in-progress', 'completed']
                if data['status'] not in valid_statuses:
                    return jsonify({'error': f'Status must be one of: {valid_statuses}'}), 400
            
            # Update task
            task.update(
                title=data.get('title', '').strip() if data.get('title') else None,
                description=data.get('description', '').strip() if data.get('description') else None,
                status=data.get('status')
            )
            
            return jsonify(task.to_dict())
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a specific task"""
    with lock:
        task_index = next((i for i, task in enumerate(tasks) if task.id == task_id), None)
        
        if task_index is None:
            return jsonify({'error': 'Task not found'}), 404
        
        deleted_task = tasks.pop(task_index)
        return jsonify({
            'message': 'Task deleted successfully',
            'deleted_task': deleted_task.to_dict()
        })

@app.route('/tasks/stats', methods=['GET'])
def get_task_stats():
    """Get task statistics"""
    with lock:
        total_tasks = len(tasks)
        pending_tasks = len([task for task in tasks if task.status == 'pending'])
        in_progress_tasks = len([task for task in tasks if task.status == 'in-progress'])
        completed_tasks = len([task for task in tasks if task.status == 'completed'])
        
        return jsonify({
            'total_tasks': total_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
        })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Task Manager API...")
    print("Available endpoints:")
    print("  GET    /           - Health check")
    print("  GET    /tasks      - Get all tasks")
    print("  POST   /tasks      - Create new task")
    print("  GET    /tasks/<id> - Get specific task")
    print("  PUT    /tasks/<id> - Update specific task")
    print("  DELETE /tasks/<id> - Delete specific task")
    print("  GET    /tasks/stats - Get task statistics")
    print("\nServer running on http://0.0.0.0:8000")
    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)