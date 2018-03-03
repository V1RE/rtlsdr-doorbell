#!/usr/bin/python3
import doorbell_config as cfg
import boto
import time
import threading
import matplotlib
matplotlib.use('Agg')
from datetime import datetime
from rtlsdr import *
from amcrest import AmcrestCamera
from twilio.rest import Client
from boto.s3.key import Key
from matplotlib.pyplot import psd

###############################################################################
# API Connections - Global
###############################################################################
global twilio
global bucket
global camera

# Twilio API
twilio = Client(cfg.TWILIO_ACCOUNT_SID, cfg.TWILIO_AUTH_TOKEN)

# AWS S3 Connection
s3 = boto.connect_s3(cfg.AWS_ACCESS_KEY_ID,cfg.AWS_SECRET_ACCESS_KEY)
bucket = s3.get_bucket(cfg.AWS_BUCKET_NAME)

# Amcrest Cameras
camera = AmcrestCamera(cfg.AMCREST_IP, 80, cfg.AMCREST_USER, cfg.AMCREST_PASS).camera


###############################################################################
# Logging Helper Function 
###############################################################################
def log(out):
    print(str(datetime.now()) + " " + out)



###############################################################################
# Doorbell Thread Alert Thread
###############################################################################

class doorbell_alert (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log("event=doorbell_rang")
        
        # Array of snapshots taken and uploaded to S3
        snaps = []

        for camid in cfg.AMCREST_CAMERAS:
            # Take a snapshot
            outfile = "doorbell_" + str(camid) + "_" + str(int(time.time())) + ".jpg"
            camera.snapshot(camid , "/tmp/" + outfile)
            log("Saved camera snapshot to: /tmp/" + outfile)

            # Upload to S3
            s3file = Key(bucket)
            s3file.key = outfile
            s3file.set_contents_from_filename("/tmp/" + outfile)
            # Get the S3 URL
            s3file_url = s3file.generate_url(expires_in = 60)
            log("Got S3 URL: " + s3file_url)
            snaps.append(s3file_url)

        # Send Text Message to targets
        for contact in cfg.TWILIO_SEND_TO:
            # Send Message Text 
            message = twilio.messages.create(
                contact,
                body = "Someone is at the door!",
                from_ = cfg.TWILIO_SEND_FROM
            )

            # Send Snapped Images
            for camid, snap in enumerate(snaps):
                log("Sending camid=" + str(camid) + ", url=" + snap + " to_phone=" + contact)

                twilio.messages.create(
                    contact,
                    body = "Camera #" + str(camid) + " - " + str(datetime.now()),
                    from_ = cfg.TWILIO_SEND_FROM,
                    media_url = snap 
                )

            log("Sent text message to_phone=" + contact)

        log("event=threadsleep_start status=blocking")
        time.sleep(10)
        log("event=threadsleep_end status=ready")


###############################################################################
# RTLSDR Setup 
###############################################################################
sdr = RtlSdr(cfg.RTLSDR_DEVICE)
sdr.sample_rate = 2.048e6 #2.048e6  # Hz
sdr.center_freq = cfg.RTLSDR_FREQ 
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

###############################################################################
# Main Loop
###############################################################################
log("event=mainloop_start")
while True:
    time.sleep(0.05)
    samples = sdr.read_samples(512)
    scan, f = psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    for s in scan:
        if s > 10 and threading.active_count() == 1: 
            alertThread = doorbell_alert()
            alertThread.start()




