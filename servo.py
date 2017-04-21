import time
import RPi.GPIO as GPIO

class Servo:
	@staticmethod
	def open():
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(3, GPIO.OUT)
		pwm = GPIO.PWM(3, 50)
		pwm.start(7.5)

		try:
		  pwm.ChangeDutyCycle(2.5)  # turn towards 2.5 = 0 degree
		  time.sleep(0.5)
		  pwm.ChangeDutyCycle(7.5) # turn towards 7.5 = 90 degree
		  time.sleep(1)
		  response = (True, 'HAITI: Ad-hoc feed has run succesfully!')
		except Exception, e:
		  response = (False, 'HAITI: Ad-hoc feed could not run: %s', e)
		finally:
		  pwm.stop()
		  GPIO.cleanup()
		  
		return response
