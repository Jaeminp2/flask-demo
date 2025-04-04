from flask import Blueprint, render_template, request, redirect, url_for
from models import db
from models.models import Todo

todo_bp = Blueprint('todo_bp', __name__, url_prefix='/todo')

@todo_bp.route('/')
def todo_page():
    todos = Todo.query.order_by(Todo.id.desc()).all()
    return render_template('todo.html', todos=todos)

@todo_bp.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('todo_bp.todo_page'))

@todo_bp.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('todo_bp.todo_page'))

@todo_bp.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.is_done = not todo.is_done
        db.session.commit()
    return redirect(url_for('todo_bp.todo_page'))
