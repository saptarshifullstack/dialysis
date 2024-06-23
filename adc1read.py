import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus with the specific address
ads = ADS.ADS1115(i2c, address=0x49)

# Set the gain to 2/3 to allow measurements up to 6.144V
ads.gain = 2/3

# Create single-ended input on channels 0, 1, and 2
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)

# Main loop
while True:
    voltage0 = chan0.voltage
    voltage1 = chan1.voltage
    voltage2 = chan2.voltage
    
    print(f"Channel P0: {voltage0:.6f}V")
    print(f"Channel P1: {voltage1:.6f}V")
    print(f"Channel P2: {voltage2:.6f}V")
    
    time.sleep(1)
