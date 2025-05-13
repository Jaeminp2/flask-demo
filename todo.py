from todo_models import db, Todo, Category
from flask import Blueprint, request, redirect, url_for, flash, render_template

todo_bp = Blueprint('todo', __name__)

# Add/delete categories
@todo_bp.route('/categories', methods=['POST'])
def add_category():
    name = request.form.get('category_name', '').strip()
    if name and not Category.query.filter_by(name=name).first():
        db.session.add(Category(name=name))
        db.session.commit()
        flash(f'Category "{name}" added.')
    else:
        flash('Invalid or duplicate category.')
    return redirect('/')

@todo_bp.route('/categories/<int:cat_id>/delete', methods=['POST'])
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    flash(f'Category "{cat.name}" deleted.')
    return redirect('/')

# View and add tasks
@todo_bp.route('/todos', methods=['POST'])
def todos():
    text   = request.form['todo'].strip()
    cat_id = request.form.get('category_id', type=int)
    if text:
        db.session.add(Todo(text=text, category_id=cat_id or None))
        db.session.commit()
        flash('Task added.')
    return redirect('/')

# Delete task
@todo_bp.route('/todos/<int:todo_id>/delete', methods=['POST'])
def delete_task(todo_id):
    task = Todo.query.get_or_404(todo_id)
    db.session.delete(task)
    db.session.commit()
    flash(f'Task "{task.text}" deleted.')
    return redirect('/')

# "Completed" toggle
@todo_bp.route('/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle(todo_id):
    t = Todo.query.get_or_404(todo_id)
    t.completed = not t.completed
    db.session.commit()
    return redirect('/')
