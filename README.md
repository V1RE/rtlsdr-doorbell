# What is this?
I have [one of these doorbells](http://amzn.to/2FabLl7) that I got on Amazon. 

I'm listening on the frequency that it broadcasts on when the button is pushed to trigger some tasks for
my home security automation. 

You probably can't use this directly, but feel free to modify it and use it as you wish.


# Requirements

* An RTL-SDR USB dongle
* A doorbell like the one mentioned above
* A machine with Python3

I had to install the following OS packages. On Ubuntu or other Debian-based distros, `apt-get install` the following:

* python3-tk
* librtlsdr0

The following Python packages. You can `pip install` the following:

* boto
* matplotlib
* numpy
* scipy
* pyrtlsdr
* amcrest
* twilio

# Configuration
Copy `doorbell_config.template.py` to `doorbell_config.py` and adjust the variables as needed.

You'll need API credentials for the Amcrest cameras, AWS (IAM role will need to have at least the ability to write to a bucket), and Twilio.


# How it works

1. Main loop listens for activity in the specified frequency
2. When a spike is detected, a thread is kicked off.
3. Thread loops through the specified cameras, saving the snapshots to `/tmp`.
4. Snapshots are uploaded to an S3 bucket.
5. Thread loops through the specified phone numbers, texting an intro message and each of the snapshots via Twilio's messaging API. 



# License
MIT License, do whatever you want. See LICENSE file for details. 
