#!/usr/bin/env python3
import time
import threading
import matplotlib
matplotlib.use('Agg')
from datetime import datetime
from rtlsdr import *
from matplotlib.pyplot import psd

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
        log("event=doorbell_alert_run")
        log("event=threadsleep_start")
        time.sleep(10)
        log("event=threadsleep_end")
        log("event=doorbell_alert_exit")
        return

###############################################################################
# RTLSDR Setup
###############################################################################
serial_numbers = RtlSdr.get_device_serial_addresses()
log(str(serial_numbers))
sdr = RtlSdr(serial_number='00000001')
sdr.sample_rate = 2.048e6
sdr.center_freq = 433.0e6
sdr.freq_correction = 60
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
