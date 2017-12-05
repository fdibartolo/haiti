from flask import Flask, request, render_template, Response
import logging
from servo import Servo
from importlib import import_module
import os
from camera_pi import Camera
app = Flask(__name__)

logging.basicConfig(filename='log/haiti.log', format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

@app.route("/")
def index():
  file = open("log/haiti.log", "r")
  lines = file.readlines()
  return render_template('index.html', lines=filter(lambda l: 'HAITI:' in l, lines)[::-1])

@app.route('/feed', methods=['POST'])
def feed():
  if valid_request(request.get_json()['key']):
    success, message = Servo.open()
    logging.info(message) if success else logging.error(message)
    return message
  else:
    logging.warning('HAITI: Invalid key for feed action!')
    return 'Error'

def valid_request(key):
  return key == 'haitimorfeta'

@app.route('/video')
def video():
  return render_template('video.html')

@app.route('/video_feed')
def video_feed():
  return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
  while True:
    frame = camera.get_frame()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/test")
def test():
  logging.info('HAITI: logging test!')
  return "Testing 1 2 3!"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
