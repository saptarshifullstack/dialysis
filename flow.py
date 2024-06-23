import RPi.GPIO as GPIO
import time
import sys

FLOW_SENSOR_GPIO = 20

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global count
count = 0
start_counter = 0

def countPulse(channel):
    global count
    if start_counter == 1:
        count += 1

# Set up event detection on the GPIO pin
try:
    GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)
except RuntimeError as e:
    print(f'Runtime error: {e}')
    GPIO.cleanup()
    sys.exit()

try:
    while True:
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        flow = (count / 7.5)  # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        print("The flow is: %.3f Liter/min" % (flow))
        count = 0
        time.sleep(1)
except KeyboardInterrupt:
    print('\nKeyboard interrupt!')
    GPIO.cleanup()
    sys.exit()
except RuntimeError as e:
    print(f'Runtime error: {e}')
    GPIO.cleanup()
    sys.exit()
