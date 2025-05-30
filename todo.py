from todo_models import db, Todo, Category
from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_wtf.csrf import generate_csrf

todo_bp = Blueprint('todo', __name__)

# Add/delete categories
@todo_bp.route('/categories', methods=['POST'])
def add_category():
    name = request.form.get('category_name', '').strip()
    if name and not Category.query.filter_by(name=name).first():
        new_cat = Category(name=name)
        db.session.add(new_cat)
        db.session.commit()
        return jsonify({
            'id': new_cat.id,
            'name': new_cat.name,
            'csrf_token': generate_csrf()
        }), 201
    return jsonify({'error': 'Invalid or duplicate category'}), 400

@todo_bp.route('/categories/<int:cat_id>/delete', methods=['POST'])
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'message': f'Category "{cat.name}" deleted'}), 200

# View and add tasks
@todo_bp.route('/todos', methods=['POST'])
def todos():
    text   = request.form['todo'].strip()
    cat_id = request.form.get('category_id', type=int)
    if text:
        new_task = Todo(text=text, category_id=cat_id or None)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            'id': new_task.id,
            'text': new_task.text,
            'completed': new_task.completed,
            'category_id': new_task.category_id,
            'toggle_url': url_for('todo.toggle', todo_id=new_task.id),
            'delete_url': url_for('todo.delete_task', todo_id=new_task.id),
            'csrf_token': generate_csrf()
        }), 201
    return jsonify({'error': 'Invalid task'}), 400

# Delete task
@todo_bp.route('/todos/<int:todo_id>/delete', methods=['POST'])
def delete_task(todo_id):
    task = Todo.query.get_or_404(todo_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task "{task.text}" deleted'}), 200

# "Completed" toggle
@todo_bp.route('/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle(todo_id):
    t = Todo.query.get_or_404(todo_id)
    t.completed = not t.completed
    db.session.commit()
    return jsonify({'completed': t.completed}), 200
