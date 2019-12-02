#!/usr/bin/python3
import os
import time
import board
import busio
import adafruit_sht31d
from datetime import datetime

ADAFRUIT_IO_KEY = 'YOUR_ADAFRUIT_IO_KEY'
# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'YOUR_ADAFRUIT_IO_USERNAME'

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor0 = adafruit_sht31d.SHT31D(i2c)
sensor1 = adafruit_sht31d.SHT31D(i2c, address = 0x45)

enclosurehumidityblack = aio.feeds('blackprinter.enclosurehumidityblack')
enclosuretemperatureblack = aio.feeds('blackprinter.enclosuretemperatureblack')
ambienthumidityblack = aio.feeds('blackprinter.ambienthumidityblack')
ambienttemperatureblack = aio.feeds('blackprinter.ambienttemperatureblack')
cputemperatureblack = aio.feeds('blackprinter.cputemperatureblack')

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

#Do the actual work
while True:
    # Get the CPU temp
    cputempblack = float(getCPUtemperature())
    atblack = 22
    ahblack = 50
    now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")
    # read the sensor with the stock i2c address
    etblack = ('%.2f'%sensor0.temperature)
    ehblack = ('%.2f'%sensor0.relative_humidity)
    #etblack = 11
    #ehblack = 44
    # read the sensor with the secondary i2c address
    atblack = ('%.2f'%sensor1.temperature)
    ahblack = ('%.2f'%sensor1.relative_humidity)
    #atblack = 11
    #ahblack = 22
    #print(now + "," + str(cputempblack) + "," + str(etblack) + "," + str(ehblack) + "," + str(atblack) + "," + str(ahblack))

    aio.send_data(enclosurehumidityblack.key, ehblack)
    aio.send_data(enclosuretemperatureblack.key, etblack)
    aio.send_data(ambienthumidityblack.key, ahblack)
    aio.send_data(ambienttemperatureblack.key, atblack)
    aio.send_data(cputemperatureblack.key, cputempblack)
    time.sleep(30)

