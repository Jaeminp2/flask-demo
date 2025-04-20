import os
from flask import Flask
from todo_models import db, Todo

# Set the secret key for our app
# Use an environment variable if available, otherwise use the development default.
SECRET_KEY = os.environ.get('SECRET_KEY', 'development-secret-key')

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from todo import todo_bp
app.register_blueprint(todo_bp)

if __name__ == '__main__':
    # Create all tables
    with app.app_context():
        db.create_all()

    print(app.url_map)

    # NOTE: Set debug to True for development mode
    app.run(host='0.0.0.0', port=5005, debug=True)
