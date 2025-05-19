# music.py
import os
from flask import Blueprint, send_file, jsonify

music_bp = Blueprint('music', __name__)
MUSIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music')

def get_music_list():
    return sorted([f for f in os.listdir(MUSIC_FOLDER) if f.lower().endswith('.mp3')])

@music_bp.route('/songs')
def list_songs():
    return jsonify(get_music_list())

@music_bp.route('/play/<filename>')
def play_music(filename):
    file_path = os.path.join(MUSIC_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='audio/mpeg')
    else:
        return 'File not found', 404
