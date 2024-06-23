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

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Main loop
while True:
    voltage = chan.voltage
    print(f"Channel P0: {voltage:.6f}V")
    time.sleep(1)