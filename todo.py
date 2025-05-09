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
    return redirect(url_for('todo.todos'))

@todo_bp.route('/categories', methods=['GET', 'POST'])
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('todo_categories'))

# View and add tasks
@todo_bp.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        text = request.form['todo']
        cat_id = request.form.get('category_id')
        item = Todo(text=text, category_id=cat_id or None)
        db.session.add(item)
        db.session.commit()
        flash('Task added')
        return redirect(url_for('todo.todos', category=cat_id))

    # GET: filter by category if provided
    cat_filter = request.args.get('category', type=int)
    query = Todo.query
    if cat_filter:
        query = query.filter_by(category_id=cat_filter)
    all_todos = query.order_by(Todo.id.desc()).all()

    categories = Category.query.order_by(Category.name).all()
    return render_template('todo.html',
                           todos=all_todos,
                           categories=categories,
                           selected=cat_filter)

# "Completed" toggle
@todo_bp.route('/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle(todo_id):
    t = Todo.query.get_or_404(todo_id)
    t.completed = not t.completed
    db.session.commit()
    return redirect(url_for('todo.todos'))
