#!/usr/bin/python3

import requests

# Set up the endpoints, which shouldn't change.
# API key and host will be passed later.
endpoint_version_info = '/api/version'
endpoint_connection_handling = '/api/connection'
endpoint_job_info = '/api/job'


class OctoPrintInfo:
    # Set up version info variables we'll modify later
    version_info_api = None             # Example: "0.1"
    version_info_server = None          # Example: "1.3.10"
    version_info_text = None            # Example: "OctoPrint 1.3.10"

    # Set up current job variables we'll modify later
    job_info_file_name = None           # Example: "whistle_v2.gcode"
    job_info_file_origin = None         # Example: "local"
    job_info_file_size = None           # Example: 1468987
    job_info_file_date = None           # Example: 1378847754

    job_info_filament_length = None     # Example: 810
    job_info_filament_volume = None     # Example: 5.36

    job_info_completion = None          # Example: 0.2298468264184775
    job_info_print_time = None          # Example: 337942
    job_info_print_time_left = None     # Example: 276

    job_info_state = None               # Example: "Printing"

    # Set up connection handling variables we'll modify later
    connection_state = None             # Example: "Operational"
    connection_port = None              # Example: "/dev/ttyACM0"
    connection_baudrate = None          # Example: 250000
    connection_printer_profile = None   # Example: "_default"

    connection_options_ports = None                       # Example: ["/dev/ttyACM0", "VIRTUAL"]
    connection_options_baudrates = None                   # Example: [250000, 230400, 115200, 57600, 38400, 19200]
    connection_options_printer_profiles = None            # Example: [{"name": "Default", "id": "_default"}]
    connection_options_port_preference = None             # Example: "/dev/ttyACM0"
    connection_options_baudrate_preference = None         # Example: 250000
    connection_options_printer_profile_preference = None  # Example: "_default"
    connection_options_autoconnect = None                 # Example: true

    def __init__(self, api_key, octoprint_host, update_on_creation=False):
        self.api_key = api_key
        self.octoprint_host = octoprint_host

        # As per https://docs.octoprint.org/en/master/api/general.html#authorization, we'll configure
        # a session to automatically send the api key headers with each request.
        self.session = requests.Session()
        self.session.headers.update({'X-Api-Key': self.api_key})

        if update_on_creation:
            self.update_data()

    def update_data(self):
        url_version_info = f'{self.octoprint_host}{endpoint_version_info}'
        url_job_info = f'{self.octoprint_host}{endpoint_job_info}'
        url_connection_handling = f'{self.octoprint_host}{endpoint_connection_handling}'

        ################################
        # Update version info data
        request_version_info = self.session.get(url_version_info)
        version_info_data = request_version_info.json()
        self.version_info_api = version_info_data.get('api')
        self.version_info_server = version_info_data.get('server')
        self.version_info_text = version_info_data.get('text')

        ################################
        # Update job data
        request_job_info = self.session.get(url_job_info)
        job_info_data = request_job_info.json()
        self.job_info_file_name = job_info_data.get('job', {}).get('file', {}).get('name')
        self.job_info_file_origin = job_info_data.get('job', {}).get('file', {}).get('origin')
        self.job_info_file_size = job_info_data.get('job', {}).get('file', {}).get('size')
        self.job_info_file_date = job_info_data.get('job', {}).get('file', {}).get('date')
        #self.job_info_filament_length = job_info_data.get('job', {}).get('filament', {}).get('length')
        #self.job_info_filament_volume = job_info_data.get('job', {}).get('filament', {}).get('volume')
        self.job_info_completion = job_info_data.get('progress', {}).get('completion')
        self.job_info_print_time = job_info_data.get('progress', {}).get('printTime')
        self.job_info_print_time_left = job_info_data.get('progress', {}).get('printTimeLeft')
        self.job_info_state = job_info_data.get('state', {})

        ################################
        # Update connection data
        request_connection_handling = self.session.get(url_connection_handling)
        connection_data = request_connection_handling.json()
        self.connection_state = connection_data.get('current', {}).get('state')
        self.connection_port = connection_data.get('current', {}).get('port')
        self.connection_baudrate = connection_data.get('current', {}).get('baudrate')
        self.connection_printer_profile = connection_data.get('current', {}).get('printerProfile')

        self.connection_options_ports = connection_data.get('options', {}).get('ports')
        self.connection_options_baudrates = connection_data.get('options', {}).get('baudrates')
        self.connection_options_printer_profiles = connection_data.get('options', {}).get('printerProfiles')
        self.connection_options_port_preference = connection_data.get('options', {}).get('portPreference')
        self.connection_options_baudrate_preference = connection_data.get('options', {}).get('baudratePreference')
        self.connection_options_printer_profile_preference = connection_data.get('options', {}).get(
            'printerProfilePreference')
        self.connection_options_autoconnect = connection_data.get('options', {}).get('autoconnect')

