from flask import Blueprint, render_template, request, jsonify
import time

timer_bp = Blueprint('timer_bp', __name__, url_prefix='/timer')

start_time = None
duration = 0

@timer_bp.route('/')
def timer_page():
    return render_template('timer.html')

@timer_bp.route('/start', methods=['POST'])
def start_timer():
    global start_time, duration
    data = request.json
    duration = int(data['duration'])
    start_time = time.time()
    return jsonify({'status': 'started'})

@timer_bp.route('/remaining')
def get_remaining():
    if start_time is None:
        return jsonify({'time': 0})
    elapsed = time.time() - start_time
    remaining_time = max(0, int(duration - elapsed))
    return jsonify({'time': remaining_time})
