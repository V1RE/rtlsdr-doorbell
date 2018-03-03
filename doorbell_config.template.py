#!/usr/bin/python3

# RTLSDR
RTLSDR_DEVICE = 0
RTLSDR_FREQ = 430.0e6 # = 430.0 MHz

# AWS
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_BUCKET_NAME = ""

# Twilio 
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_SEND_FROM = ""
TWILIO_SEND_TO = [
    "",
    "",
] # phone numbers to send to. Add as many as needed to your array.

# Amcrest DVR
AMCREST_IP = ""
AMCREST_USER = ""
AMCREST_PASS = ""
AMCREST_CAMERAS = [0,1] # Cameras to query. Add more as needed.

