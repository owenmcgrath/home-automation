import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

for i in range (5):
	GPIO.output(11, GPIO.HIGH)
	print("relay high")
	time.sleep(2.5)
	GPIO.output(11, GPIO.LOW)
	print("relay low");
	time.sleep(2.5)



print("done")
