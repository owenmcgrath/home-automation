import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

def UpdateOledDisplay(oled, setting, temp):
	# Clear display.
	oled.fill(0)
	oled.show()

	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	image = Image.new('1', (oled.width, oled.height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	# Draw a black background
	draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)


	# Load default font.
	font = ImageFont.load_default()

	# Draw Some Text
	text = "Room Temp: " + str(temp) + " *F"
	text2 = "Setting: " str(setting) + " *F"

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
	return temperature



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

	"""
	DHT22 CONFIG
	"""
	DHT_SENSOR = Adafruit_DHT.DHT22
	DHT_PIN = 22

	"""
	BUTTON CONFIG
	"""
	UP_BUTTON_PIN = 13
	DOWN_BUTTON_PIN = 15

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	"""
	RELAY CONFIG
	"""
	RELAY_PIN = 11
	GPIO.setup(11, GPIO.OUT)

	"""
	RUN THE THERMOSTAT!
	"""
	currSetting = 75
	currTemp = 0
	lastDownButtonState = False
	lastUpButtonState = False
	lineOpen = False
	lastLoopTime = 0
	while True:
		
		#get the button input and update the current thermostat setting based on that
		upButtonState = GPIO.input(13) == GPIO.HIGH
		downButtonState = GPIO.input(15) == GPIO.HIGH
		if (not lastDownButtonState) and downButtonState:
			currSetting++
			UpdateOledDisplay(oled,setting, time)
		if (not lastUpButtonState) and  upButtonState:
			currSetting--
			UpdateOledDisplay(oled, setting, time)
		lastUpButtonState = upButtonState
		lastDownButtonState = downButtonState

		#every second update the relay state
		if time.time() - lastLoopTime > 1:

			currTemp = GetTemp(DHT_SENSOR, DHT_PIN)
			lineOpen = currTemp < setting

			GPIO.output(GPIO.HIGH if lineOpen else GPIO.LOW)
			UpdateOledDisplay(oled, currSetting, currTemp)
			lastLoopTime = time.time()


