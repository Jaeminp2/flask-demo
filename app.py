import os
from flask import Flask, render_template
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
from timer import timer_bp         # timer 블루프린트 임포트
app.register_blueprint(todo_bp)
app.register_blueprint(timer_bp)  # 블루프린트 등록


@app.route('/')
def home():
    return render_template('main.html')

# if __name__ == '__main__':
#     # Create all tables
#     with app.app_context():
#         db.create_all()

#     print(app.url_map)

#     # NOTE: Set debug to True for development mode
#     app.run(host='0.0.0.0', port=5005, debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    print(app.url_map)  # 등록된 라우트 목록 확인

    app.run(debug=True)
