"""
Time-traveling clock for Studio Aspekto
"""

import datetime
import threading

from flask import Flask, request

app = Flask(__name__)

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


@app.route('/time', methods=["GET", "POST"])
def time():
    """
    set or get the current timestamp
    """
    global TIME
    if request.method == 'POST':
        TIME = datetime.datetime.strptime(request.json['time'][:-7], "%Y-%m-%dT%H:%M:%S")

    return TIME.isoformat()

@app.route('/delta', methods=["GET", "POST"])
def delta():
    """
    set or get the amount of seconds to be added every second
    """
    global TIMEDELTA
    if request.method == 'POST':
        TIMEDELTA = float(request.json["delta"])

    return str(TIMEDELTA)

if __name__ == '__main__':
    tick()
    app.run('0.0.0.0', 3000)
