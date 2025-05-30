import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from todo_models import db, Category

SECRET_KEY = os.environ.get('SECRET_KEY', 'development-secret-key')
app = Flask(__name__)
app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)

# DB 기본 세팅
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 블루프린트 파트
from todo import todo_bp
from timer import timer_bp
from study_stats import study_bp
from music import music_bp

app.register_blueprint(todo_bp)
app.register_blueprint(timer_bp)
app.register_blueprint(study_bp)
app.register_blueprint(music_bp)

@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('main.html', categories=categories)

#앱실행 파트
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    print(app.url_map)
    app.run(debug=True)
