from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Todo: {self.text} completed={self.completed}>"
