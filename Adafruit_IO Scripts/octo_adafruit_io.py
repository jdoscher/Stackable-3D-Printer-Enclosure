#!/usr/bin/python3
import time
import datetime

from octoprint_info import OctoPrintInfo

# Create our OctoPrintInfo instance. Be sure to set up the API key and host accordingly.
# For the host, you may also need to set up the port, e.g. 'http://192.168.13.37:7070'
octoprint_info = OctoPrintInfo(api_key='YOUR_API_KEY_HERE', octoprint_host='http://YOUR_OCTOPPRINT_SERVER_IP:5000')

ADAFRUIT_IO_KEY = 'YOUR_ADAFRUIT_IO_KEY'
# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'YOUR_ADAFRUIT_IO_USERNAME'

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
blackprintremaining = aio.feeds('blackprinter.blackprinttimeremaining')
#blackprinterstate = aio.feeds('blackprinter.blackprinterstate')
#blackconnectstate = aio.feeds('blackprinter.blackprinterstate')

# Update info and display a couple of fields every sixty seconds
while True:
    octoprint_info.update_data()
    #print(str(datetime.timedelta(seconds=octoprint_info.job_info_print_time_left)))
    printremaining = (str(datetime.timedelta(seconds=octoprint_info.job_info_print_time_left)))
    #printerstate = (octoprint_info.job_info_state)
    #connectstate = (octoprint_info.connection_state)
    #print(printremaining)
    aio.send_data(blackprintremaining.key, printremaining)
    #aio.send_data(blackprinterstate.key, printerstate)
    #aio.send_data(blackconnectstate.key, connectstate)
    time.sleep(120)
