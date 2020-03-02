"""
This demo will fill the screen with white, draw a black box on top
and then print Hello World! in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32     # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3d, reset=oled_reset)

# Use for SPI
#spi = board.SPI()
#oled_cs = digitalio.DigitalInOut(board.D5)
#oled_dc = digitalio.DigitalInOut(board.D6)
#oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

# Draw a smaller inner rectangle
#draw.rectangle((BORDER, BORDER, oled.width - BORDER, oled.height - BORDER),
#               outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()

# Draw Some Text
text = "Room Temp: 75 *F"
text2 = "Setting: 65 *F"

(font_width, font_height) = font.getsize(text)
draw.text((oled.width//2 - font_width//2, 3*oled.height//4 - font_height//2),
          text2, font=font, fill=255)

draw.text((oled.width//2 - font_width//2, oled.height//4 - font_height//2), text, font = font, fill = 255)

# Display image
oled.image(image)
oled.show()
