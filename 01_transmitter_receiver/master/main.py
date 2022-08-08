# This file is an example of two way communication
# Master

from machine import UART, Pin
import time
from micropython import const

# RS485 control
print('Setting pins')
ctrl_pin = Pin(33, Pin.OUT)
tx_pin_value = const(1)
rx_pin_value = const(0)

uart = UART(1, 9600, bits=8, parity=None, stop=1, tx=25, rx=32)

print('seting up')
ctrl_pin.value(rx_pin_value)
time.sleep_ms(500)

ctrl_pin.value(tx_pin_value)
print('Send Data')
uart.write(b'Hello World!')

time.sleep_ms(500)


buff = bytearray(50)

print('Waiting for response...\n')
for i in range(500):
    ctrl_pin.value(rx_pin_value)

    data_avail = uart.any() # Gets number of characters which can be read from UART

    if data_avail > 0 :
        print(f'Characters available: {data_avail}')
        uart.readinto(buff)
        print(f'{buff[0 : data_avail]} \n')
        buff[:] = b'\x00' * len(buff)


    time.sleep_ms(200)

print('Completed test.')