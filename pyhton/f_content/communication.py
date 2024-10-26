## This will be responsible for the communication protocols between the hardware and the software

## Implement the I2C communication protocol

''' Documentation: 
- smbus2 library: https://pypi.org/project/smbus2/
- Interfacing with hardware1: https://www.abelectronics.co.uk/kb/article/1094/i2c-part-4-programming-i2c-with-python
- Interfacing with hardware2: https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all
'''

import smbus2 ## Used for accessing the system I2C bus (improvement over smbus)
import time ## Used for time delays

## Important instructions for the I2C communication protocol and the library in https://pypi.org/project/smbus2/

class I2C:
    ## Constructor
    def __init__(self, address,bus = None):
        self.address = address
        self.bus = bus
        self.o_smbus = smbus2.SMBus(bus)

    ## Method to write data to the I2C bus
    def write(self, data):
        self.o_smbus.write_i2c_block_data(self.address, 0, data) ## 0 is the offset
    
    ## Method to read data from the I2C bus
    def read(self, length): # length in bytes, max = 32, but not recommended without a delay
        self.r_data = self.o_smbus.read_i2c_block_data(self.address, 0, length) ## 0 is the offset

    
    ## TODO: If we have bulk messages we can use the i2c_msg class, for this check the library documentation
