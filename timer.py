from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

TODO_FILE = "todo.txt"

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/timer')
def timer():
    return render_template('timer.html')

if __name__ == '__main__':
    app.run(debug=True)
