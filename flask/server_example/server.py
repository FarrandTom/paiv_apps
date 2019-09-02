# dont need fps, camera, base_camera, inference helper

#from camera import Camera #don't need this
#from camera import inference_thread #don't understand this

import logging #for debugging
import time #time related tasks
import numpy as np
import requests
import cv2
import json
import base64
import io
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from flask import Flask, render_template, request, Response, make_response
from werkzeug import secure_filename

POWERAI_BASEURL = "http://9.196.150.55:8007/inference"

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Server")

# 'UPLOAD_FOLDER ='/Uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif', 'png'])

app = Flask(__name__)
#app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER
os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

ENDPOINT = "http://9.196.150.55:8007/inference"
def infer_image(frame):
    """
    Send a frame for inference at the backend.
    """
    endpoint = "https://9.196.150.153/powerai-vision/api/dlapis/da535e14-2ff6-4ed4-8d95-653405276ad8"
    #file = frame.read()
    #print(file)
    myfiles = {'files': (frame)}

    status_code = 0
    retry_count = 0
    resp_value = dict()
    objs = None

    while (status_code != 200) and (retry_count < 5) and (objs is None):
        try:
            if retry_count != 0:
                logger.warning(f"retrying upload for {frame}, attempt {retry_count}")
            #print(myfiles)
            request = requests.post(endpoint, files=myfiles, verify=False) #both were frame
            status_code = request.status_code
            retry_count = retry_count + 1
            #file.close()
            #print(request.text)
            resp_value = json.loads(request.text)

            if 'classified' in resp_value.keys():
                objs = resp_value['classified']

        except Exception as e:
            logger.exception("Caught exception during inference API call.")
            pass

    if objs is None:
        objs = []

    return status_code, objs

@app.route('/') #when home page of web server is opened in browser, index.html will be rendered
def index():
    return render_template('index.html', label="")

@app.route('/upload')
def upload():
   return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save('upload_test.jpg')

      image = open('upload_test.jpg', 'rb')
      my_files = {'files': ('Uploaded photo', image)}
      my_request = requests.post(ENDPOINT, files=my_files, verify=False)
      resp_value = json.loads(my_request.text)
      #for x in resp_value:
        #print(x)
      print(resp_value)
      #seperate response into each label
      # for each label
      # draw rectangle based on number

      cv2_image = cv2.imread('upload_test.jpg')
      #print(type(cv2_image))
      #print((len(resp_value['classified'])))
      bound= len(resp_value['classified'])
      font = cv2.FONT_HERSHEY_SIMPLEX
      for x in range(0, bound):
        print((resp_value['classified'][0]['label']))
        x_max = resp_value['classified'][x]['xmax']
        y_max = resp_value['classified'][x]['ymax']
        x_min = resp_value['classified'][x]['xmin']
        y_min = resp_value['classified'][x]['ymin']

        if resp_value['classified'][x]['label'] == 's822l': #or 's822':
            print('ok')
            cv2.rectangle(cv2_image, (x_max,y_max), (x_min, y_min),(0,255,0),30)
            cv2.rectangle(cv2_image, (x_min,y_min), (x_min+500, y_min-100),(0,255,0),-1)
            cv2.putText(cv2_image,'s822',(x_min,y_min), font, 4,(255,255,255),15,cv2.LINE_AA)
            server= 's822'
        elif resp_value['classified'][x]['label'] == 's822':
            print('no')
            cv2.rectangle(cv2_image, (x_max,y_max), (x_min, y_min),(255,0,0),30)
            cv2.rectangle(cv2_image, (x_min,y_min), (x_min+500, y_min-100),(255,0,0),-1)
            cv2.putText(cv2_image,'s822',(x_min,y_min), font, 4,(255,255,255),15,cv2.LINE_AA)
            server= 's822'
        elif resp_value['classified'][x]['label'] == 'storwize':
             print('id')
             cv2.rectangle(cv2_image, (x_max,y_max), (x_min, y_min),(0,0,255),30)
             cv2.rectangle(cv2_image, (x_min,y_min), (x_min+500, y_min-100),(0,0,255),-1)
             cv2.putText(cv2_image,'storwize',(x_min,y_min), font, 4,(255,255,255),15,cv2.LINE_AA)
             server= 'storwize'
        else:
            print('id')
            cv2.rectangle(cv2_image, (x_max,y_max), (x_min, y_min),(255,0,255),30)
            cv2.rectangle(cv2_image, (x_min,y_min), (x_min+150, y_min-100),(255,0,255),-1)
            cv2.putText(cv2_image,'id',(x_min,y_min), font, 4,(255,255,255),15,cv2.LINE_AA)

#       cv2.textbox


# {'classified': [{'confidence': 0.99891, 'ymax': 1574, 'label': 's822l', 'xmax': 3897, 'xmin': 240, 'ymin': 822, 'attr': [{}]}, {'confidence': 0.99816, 'ymax': 2190, 'label': 's822', 'xmax': 3815, 'xmin': 326, 'ymin': 1554, 'attr': [{}]}], 'result': 'success'}

      #print(type(cv2.line))
      buffer = cv2.imencode('.jpg', cv2_image)[1]
      #cv2.line(cv2_image,(0,0),(511,511),(255,0,0),5)[1]
      #encoded_image = cv2.imencode('.jpg', cv2_image)[1].tostring()
      #encoded_image = cv2.imencode('.jpg', cv2_image)

      b64_image = base64.b64encode(buffer)
      #print(encoded_image)
      b64_image = b64_image.decode("utf-8")
      #print(b64_image.decode("utf-8"))
      #b64_image = base64.b64encode(encoded_image)
      #write to output file
      #check if its what we want


      # #File-storage -> numpy
      # array = np.frombuffer(f.read(), dtype=np.uint16)
      #
      # # Seek back to the beginning of the stream
      # f.seek(0)
      #
      # # Load into an in-memory buffer, this then is fed to the inference API
      # in_memory_file = io.BufferedReader(f)
      # my_files = {'files': ('Uploaded photo', in_memory_file)}
      # my_request = requests.post(ENDPOINT, files=my_files, verify=False)
      # resp_value = json.loads(my_request.text)
      # print(resp_value)
      #
      # # Use the resp_value coordinates to draw bounding boxes on image np.array
      # # ...
      # cv2.line(array,(0,0),(511,511),(255,0,0),5)
      # cv2.imwrite('upload.jpg', array)
      #
      # # Rendering the drawn cv2 image
      # #b64_image = "data:image/png;base64, " + base64.b64encode(array).decode("utf-8")
      # #print(b64_image[0:100])

      return render_template('index.html', response_image=b64_image, server=server)

# if __name__ == '__main__':
#    app.run(debug = True)

#
# @app.route('/uploader')
# def upload_file():
#
#     if request.method == 'POST':
#         print('here')
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             #send for inference
#             console.log('here')
#             status_code, json_resp = infer_image(file)
#             print(status_code, json_resp)
#             console.log('sent to infer_image')


#@app.route('/upload')
#def upload_file():
#   return render_template('upload.html')

#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_file():
#   if request.method == 'POST':
#      f = request.files['file']
#      f.save(secure_filename(f.filename))
#      return 'file uploaded successfully'

#if __name__ == '__main__':
#   app.run(debug = True)

@app.route('/capture') #this is reading the json response and changing the html
def capture():
    # Need to capture the current json_resp(onse) which is already being held in the
    # drawing helper thread. Therefore need access to that thread's queue.
    json_resp = inference_thread.json_resp #json endpoint

    if json_resp:
        label = json_resp[0]['label']
        aisle = ""
    else:
        label = ""
        aisle = ""

    if label == "s822":
        aisle = "four"
        print('heyheyyyy')
    elif label == "s822l":
        aisle = "eight"
        print('hej')

    return render_template('index.html', label=label, aisle=aisle)

#def gen(camera):
#    """Video streaming generator function."""
#    while True:
#        frame = camera.get_frame()
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#@app.route('/video_feed')
#def video_feed():
#    return Response(gen(Camera()),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=False)
