from flask import request, jsonify
from src.models import db, Task

def init_routes(app):
    @app.route('/tasks', methods=['POST'])
    def add_task():
        data = request.get_json()
        title = data.get("title")
        if title:
            task = Task(title=title)
            db.session.add(task)
            db.session.commit()
            return jsonify(task.to_dict()), 201
        return jsonify({"error": "Title is required"}), 400

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        task.completed = data.get("completed", task.completed)
        db.session.commit()
        return jsonify(task.to_dict())

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"})
