# music.py

from flask import Blueprint, send_file
import os

music_bp = Blueprint("music", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MUSIC_PATH = os.path.join(BASE_DIR, 'music', '여행 릴러말즈.mp3')

@music_bp.route("/music")
def music():
    return send_file("/Users/jaeminpark/Desktop/flask-demo/music/겨울카페 분위기.mp3", mimetype='audio/mpeg', as_attachment=False)
