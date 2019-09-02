from camera import Camera
from camera import inference_thread

import logging
import time

import cv2

from flask import Flask, render_template, Response

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Server")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', label="", aisle="")

@app.route('/capture')
def capture():
    # Need to capture the current json_resp which is already being held in the
    # drawing helper thread. Therefore need access to that thread's queue.
    json_resp = inference_thread.json_resp
    
    if json_resp:
        label = json_resp[0]['label']
        aisle = ""
    else:
        label = ""
        aisle = ""

    if label == "pliers":
        aisle = "four"
    elif label == "spanners":
        aisle = "eight"

    return render_template('index.html', label=label, aisle=aisle)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
