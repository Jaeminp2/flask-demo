from flask import Flask, render_template
from flask_socketio import SocketIO
from models import db
from models.models import Todo
from timer import timer_bp
from todo import todo_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app)  # ✅ 소켓 서버로 Flask 래핑

app.register_blueprint(timer_bp)
app.register_blueprint(todo_bp)

@app.route('/')
def main():
    return render_template('main.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)  # ✅ 여기 중요!!
