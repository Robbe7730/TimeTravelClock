"""
Time-traveling clock for Studio Aspekto
"""

import datetime
import threading

from flask import Flask, request, redirect

app = Flask(__name__, static_url_path='')

TIME = datetime.datetime.now()
TIMEDELTA = 1

def tick():
    """
    called every second
    """
    global TIME
    global TIMEDELTA

    TIME += datetime.timedelta(seconds=TIMEDELTA)

    threading.Timer(1, tick, []).start()

@app.route('/')
def index():
    return redirect('index.html')

@app.route('/time', methods=["GET", "POST"])
def time():
    """
    set or get the current timestamp
    """
    global TIME
    if request.method == 'POST':
        TIME = datetime.datetime.strptime(request.form['time'], "%H:%M:%S")
        return redirect('admin.html')

    return TIME.isoformat()

@app.route('/delta', methods=["GET", "POST"])
def delta():
    """
    set or get the amount of seconds to be added every second
    """
    global TIMEDELTA
    if request.method == 'POST':
        TIMEDELTA = float(request.form["delta"])
        return redirect('admin.html')

    return str(TIMEDELTA)

if __name__ == '__main__':
    tick()
    app.run('0.0.0.0', 3000)
