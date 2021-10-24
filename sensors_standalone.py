#!/usr/bin/env python3
import time
import colorsys
import sys
import ST7735
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
from subprocess import PIPE, Popen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from fonts.ttf import RobotoMedium as UserFont

import socket

# Get IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = str(s.getsockname()[0])


# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# PMS5003 particulate sensor
pms5003 = PMS5003()

# Create ST7735 LCD display class
st7735 = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display
st7735.begin()

WIDTH = st7735.width
HEIGHT = st7735.height

# Set up canvas and font
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font_size = 20
font = ImageFont.truetype(UserFont, font_size)

message = ip
print(message)

# Draw on Screen
draw.text((0, 0), message, font=font, fill=(255, 255, 255))
st7735.display(img)

# The position of the top bar
top_pos = 25

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25

cpu_temps = [get_cpu_temperature()] * 5

# The main loop
try:
    while True:
        # variable = proximity
        proximity = ltr559.get_proximity()

        # variable = "temperature"
        unit = "C"
        cpu_temp = get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = bme280.get_temperature()
        temperature = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
        temperature = str(round(temperature, 2))

        # variable = "pressure"
        unit = "hPa"
        pressure = str(round(bme280.get_pressure(), 2))

        # variable = "humidity"
        unit = "%"
        humidity = str(round(bme280.get_humidity()))

        # variable = "light"
        unit = "Lux"
        light = str(round(ltr559.get_lux()))
 
        
        #print(proximity)
        print("Temperature (C): "+temperature)
        print("Pressure (hPa): "+pressure)
        print("Humidity (%): "+humidity)
        print("Light (Lux): "+light)
        
# Exit cleanly
except KeyboardInterrupt:
    sys.exit(0)
