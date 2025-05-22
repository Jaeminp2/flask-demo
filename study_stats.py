# study_stats.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from todo_models import db
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

class StudyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

study_bp = Blueprint('study', __name__)

@study_bp.route('/log', methods=['POST'])
def log_study():
    data = request.get_json()
    duration = data.get('duration')
    category_id = data.get('category_id')

    if duration is None:
        return jsonify({"error": "Duration is required"}), 400

    log = StudyLog(duration=duration, category_id=category_id or None)
    db.session.add(log)
    db.session.commit()
    return jsonify({"message": "Logged successfully"}), 200

from sqlalchemy.sql import func
from todo_models import Category

@study_bp.route('/stats', methods=['GET'])
def study_stats():
    total = db.session.query(func.sum(StudyLog.duration)).scalar() or 0
    uncategorized = db.session.query(func.sum(StudyLog.duration)) \
        .filter(StudyLog.category_id == None).scalar() or 0

    per_category = db.session.query(
        Category.name, func.sum(StudyLog.duration)
    ).join(Category, StudyLog.category_id == Category.id) \
     .group_by(Category.id).all()

    return jsonify({
        "total": total,
        "uncategorized": uncategorized,
        "by_category": [
            {"name": name, "duration": dur or 0}
            for name, dur in per_category
        ]
    })
