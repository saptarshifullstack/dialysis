import tkinter as tk
import threading
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import os
import glob
import time

# ADC setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x49)
ads.gain = 2/3

chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)

# Flow sensor setup
FLOW_SENSOR_GPIO = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
global count
count = 0
start_counter = 0

def countPulse(channel):
    global count
    if start_counter == 1:
        count += 1

GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)

# Temperature sensor setup
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Tkinter GUI setup
class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Readings")

        self.ph_label = tk.Label(root, text="pH: N/A", font=("Helvetica", 14))
        self.ph_label.pack()

        self.conductivity_label = tk.Label(root, text="Conductivity: N/A", font=("Helvetica", 14))
        self.conductivity_label.pack()

        self.pressure_label = tk.Label(root, text="Pressure: N/A", font=("Helvetica", 14))
        self.pressure_label.pack()

        self.flow_label = tk.Label(root, text="Flow: N/A", font=("Helvetica", 14))
        self.flow_label.pack()

        self.temp_label = tk.Label(root, text="Temperature: N/A", font=("Helvetica", 14))
        self.temp_label.pack()

        self.update_readings()

    def update_readings(self):
        global start_counter, count

        # Read ADC channels
        ph = chan0.voltage
        conductivity = chan1.voltage
        pressure = chan2.voltage

        # Read flow
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        flow = count / 7.5  # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min
        count = 0

        # Read temperature
        temp_c, temp_f = read_temp()

        # Update labels
        self.ph_label.config(text=f"pH: {ph:.3f}V")
        self.conductivity_label.config(text=f"Conductivity: {conductivity:.3f}V")
        self.pressure_label.config(text=f"Pressure: {pressure:.3f}V")
        self.flow_label.config(text=f"Flow: {flow:.3f} L/min")
        self.temp_label.config(text=f"Temperature: {temp_c:.3f}°C / {temp_f:.3f}°F")

        # Schedule the next update
        self.root.after(1000, self.update_readings)

def main():
    root = tk.Tk()
    app = SensorApp(root)

    # Start Tkinter main loop
    root.mainloop()

    # Cleanup GPIO on exit
    GPIO.cleanup()

if __name__ == "__main__":
    main()
