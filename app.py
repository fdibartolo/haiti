from flask import Flask, render_template
import time
import logging
import RPi.GPIO as GPIO
app = Flask(__name__)

# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
logging.basicConfig(filename='log/haiti.log', format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


@app.route("/")
def index():
   file = open("log/haiti.log", "r") 
   return render_template('index.html', lines=file.readlines())

@app.route('/feed', methods=['POST'])
def feed():
   if valid_request(request.form['key']):
      GPIO.setup(3, GPIO.OUT)
      pwm = GPIO.PWM(3, 50)
      pwm.start(7.5)

      try:
         p.ChangeDutyCycle(2.5)  # turn towards 2.5 = 0 degree
         time.sleep(0.5)
         p.ChangeDutyCycle(7.5) # turn towards 7.5 = 90 degree
         time.sleep(1)
         logging.info('Ad-hoc feed has run succesfully')
      except Exception, e:
         logging.error('Ad-hoc feed could not run: %s', e)
      finally:
         p.stop()
         GPIO.cleanup()
         return 'Ok'
   else:
      logging.warning('Invalid key for feed action!')
      return 'Error'

def valid_request(key):
   # return key == 'haitimorfeta'
   return True


@app.route("/readPin/<pin>")
def readPin(pin):
   try:
      GPIO.setup(int(pin), GPIO.IN)
      if GPIO.input(int(pin)) == True:
         response = "Pin number " + pin + " is high!"
      else:
         response = "Pin number " + pin + " is low!"
   except:
      response = "There was an error reading pin " + pin + "."

   templateData = {
      'title' : 'Status of Pin' + pin,
      'response' : response
      }

   return render_template('pin.html', **templateData)



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)
