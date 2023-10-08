import time
from FireAlarm import *
time.sleep(0.1) # Wait for USB to become ready

print("Hello Sunshine!")

myalarm = FireAlarm()
myalarm.run()

