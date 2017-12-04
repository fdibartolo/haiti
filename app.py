from flask import Flask, request, render_template
import time
import logging
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
logging.basicConfig(filename='log/haiti.log', format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

@app.route("/")
def index():
  file = open("log/haiti.log", "r")
  lines = file.readlines()
  return render_template('index.html', lines=lines[::-1])

@app.route('/feed', methods=['POST'])
def feed():
  if valid_request(request.get_json()['key']):
    GPIO.setup(3, GPIO.OUT)
    pwm = GPIO.PWM(3, 50)
    pwm.start(7.5)

    try:
      pwm.ChangeDutyCycle(2.5)  # turn towards 2.5 = 0 degree
      time.sleep(0.5)
      pwm.ChangeDutyCycle(7.5) # turn towards 7.5 = 90 degree
      time.sleep(1)
      logging.info('Ad-hoc feed has run succesfully')
    except Exception, e:
      logging.error('Ad-hoc feed could not run: %s', e)
    finally:
      pwm.stop()
      GPIO.cleanup()
      return 'Ok'
  else:
    logging.warning('Invalid key for feed action!')
    return 'Error'

def valid_request(key):
  return key == 'haitimorfeta'

@app.route("/test")
def test():
  logging.info('logging test!')
  return "Testing 1 2 3!"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
