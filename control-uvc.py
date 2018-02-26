#!/usr/bin/python3

import sys
import requests
from urllib.parse import urlunparse
# The urlparse module is renamed to urllib.parse in Python 3.
import argparse
import ipaddress

parser = argparse.ArgumentParser(description='Start or stop recording on a Unifi Video Cameras via the Unifi NVR.\n'
                                             'Useful as a helper in Home Automation software.')
parser.add_argument("nvrIP",
                    help="IP address and port of the Unifi NVR in the form n.n.n.n")
parser.add_argument("camUUID",
                    help="UUID of the camera you want to control")
parser.add_argument("camName",
                    help='Name of the camera you want to control (Will go in caption)')
parser.add_argument("apiKey",
                    help='API key issued to a user by the Unifi NVR software in Users>[User]>API Access')
parser.add_argument("action",
                    help='What you would like done to the recording function of the camera',
                    choices=['start', 'stop'])
parser.add_argument("--https",
                    help='Use HTTPS instead of HTTP when talking to the API',
                    action='store_true')
parser.add_argument('--apiport', help='Port to send API request to on the NVR.  7080 if not specified',
                    nargs='?',
                    default=7080,
                    type=int)
args = parser.parse_args()

try:
    ipaddress.ip_address(args.nvrIP)
except ipaddress.AddressValueError:
    parser.error("NVR Address doesn't appear to be a valid IP address\nPlease format like 192.168.1.100")

if args.https is True:
    proto = 'https'
else:
    proto = 'http'

urlPieces = [proto, '{0}:{1}'.format(args.nvrIP, args.apiport), '/api/2.0/camera/{0}'.format(args.camUUID), '',
             'apiKey={0}'.format(args.apiKey), '']

# urllib in Python 3, urlparse in Python 2
nvrApiUrl = urlunparse(tuple(urlPieces))

recordingSettings = {'motionRecordEnabled': False, 'channel': 0}
if args.action == "start":
    recordingSettings['fullTimeRecordEnabled'] = True
else:
    recordingSettings['fullTimeRecordEnabled'] = False
payload = {'name': args.camName, 'recordingSettings': recordingSettings}

r = requests.put(nvrApiUrl, json=payload)
if r.status_code == 200:
    sys.exit()
else:
    sys.exit('An error occurred talking to the API.\nWe got HTTP status code {0}'.format(r.status_code))
