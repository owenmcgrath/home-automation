import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

lastDownButtonState = False
lastUpButtonState = False

while True:
	upButtonState = GPIO.input(13) == GPIO.HIGH
	downButtonState = GPIO.input(15) == GPIO.HIGH
	if (not lastDownButtonState) and downButtonState:
		print("Down Button Pushed")
	if (not lastUpButtonState) and  upButtonState:
		print("Up Button Pushed")
	lastUpButtonState = upButtonState
	lastDownButtonState = downButtonState

