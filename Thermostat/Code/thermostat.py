

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

def UpdateOledDisplay(oled, font, draw, image, setting, temp):
	# Clear the image
	draw.rectangle((0, 0, oled.width, oled.height), outline = 0, fill = 0)
	# Draw the text
	text = "Room Temp: " + str(round(temp, 1)) + " *F"
	text2 = "Setting: " + str(setting) + " *F"

	(font_width, font_height) = font.getsize(text)
	draw.text((oled.width//2 - font_width//2, 3*oled.height//4 - font_height//2),
          text2, font=font, fill=255)

	draw.text((oled.width//2 - font_width//2, oled.height//4 - font_height//2), text, font = font, fill = 255)

	# Display image
	oled.image(image)
	oled.show()

def GetTemp(dhtSensor, dhtPin):
	humidity, temperature = Adafruit_DHT.read_retry(dhtSensor, dhtPin)
	if(temperature is None):
		temperature = -1 #Theres an error likely with the wiring
	return 1.8 * temperature + 32



if __name__ == "__main__":

	"""
	OLED CONFIG
	"""
	# Define the Reset Pin
	oled_reset = digitalio.DigitalInOut(board.D4)

	# Change these
	# to the right size for your display!
	WIDTH = 128
	HEIGHT = 32     # Change to 64 if needed

	# Use for I2C.
	i2c = board.I2C()
	oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3d, reset=oled_reset)

	oled.fill(0)
	oled.show()

	image = Image.new('1', (oled.width,oled.height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,oled.width,oled.height), outline = 0, fill = 0)
	font = ImageFont.load_default()

	"""
	DHT22 CONFIG
	"""
	DHT_SENSOR = Adafruit_DHT.DHT22
	DHT_PIN = 23

	"""
	BUTTON CONFIG
	"""
	UP_BUTTON_PIN = 27
	DOWN_BUTTON_PIN = 22

	GPIO.setwarnings(False)
	GPIO.setup(UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	"""
	RELAY CONFIG
	"""
	RELAY_PIN = 17
	GPIO.setup(RELAY_PIN, GPIO.OUT)

	"""
	RUN THE THERMOSTAT!
	"""
	currSetting = 75
	currTemp = GetTemp(DHT_SENSOR, DHT_PIN)
	lastDownButtonState = False
	lastUpButtonState = False
	lineOpen = False
	firstRun = True
	lastLoopTime = 0
	lastSetTime = 0
	while True:
		#get the button input and update the current thermostat setting based on that
		upButtonState = GPIO.input(UP_BUTTON_PIN) == GPIO.HIGH
		downButtonState = GPIO.input(DOWN_BUTTON_PIN) == GPIO.HIGH
		timestamp = time.time()
		if (not lastDownButtonState) and downButtonState:
			currSetting = currSetting - 1
			UpdateOledDisplay(oled, font, draw, image, currSetting, currTemp)
			lastSetTime = timestamp
		if (not lastUpButtonState) and  upButtonState:
			currSetting = currSetting + 1
			print(currSetting)
			UpdateOledDisplay(oled, font, draw, image, currSetting, currTemp)
			lastSetTime = timestamp
		lastUpButtonState = upButtonState
		lastDownButtonState = downButtonState
		noInput = (timestamp - lastSetTime) > 5
		if (lineOpen != (currTemp < currSetting)) or firstRun:
			lineOpen = currTemp < currSetting
			GPIO.output(RELAY_PIN, GPIO.HIGH if lineOpen else GPIO.LOW)
			firstRun = False
		if (timestamp - lastLoopTime) > 30 and noInput:
			lastLoopTime = timestamp
			currTemp = GetTemp(DHT_SENSOR, DHT_PIN)
			UpdateOledDisplay(oled, font, draw, image, currSetting, currTemp)
