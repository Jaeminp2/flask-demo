from todo_models import db, Todo
from flask import Blueprint, request, redirect, url_for, flash, render_template

todo_bp = Blueprint('todo', __name__)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(255), nullable=False)
#     completed = db.Column(db.Boolean, default=False)

#     def __repr__(self):
#         return f"<Todo: {self.text} completed={self.completed}>"

# View and add tasks
@todo_bp.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        new_text = request.form.get('todo')
        if new_text:
            item = Todo(text=new_text)
            db.session.add(item)
            db.session.commit()
            flash('Task added successfully')
        return redirect(url_for('todo.todos'))
    
    all_todos = Todo.query.order_by(Todo.id.desc()).all()
    return render_template('todo.html', todos=all_todos)

# "Completed" toggle
@todo_bp.route('/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle(todo_id):
    t = Todo.query.get_or_404(todo_id)
    t.completed = not t.completed
    db.session.commit()
    return redirect(url_for('todo.todos'))
