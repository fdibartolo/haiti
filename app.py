from flask import Flask, request, render_template
import logging
from servo import Servo
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

@app.route("/test")
def test():
  logging.info('HAITI: logging test!')
  return "Testing 1 2 3!"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
