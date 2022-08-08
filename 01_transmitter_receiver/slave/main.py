# This file is an example of two way communication
# Slave

from machine import UART, Pin
import time
from micropython import const

# RS485 control
print('Setting pins')
ctrl_pin = Pin(33, Pin.OUT)
tx_pin_value = const(1)
rx_pin_value = const(0)

uart = UART(1, 9600, bits=8, parity=None, stop=1, tx=25, rx=32)

print('setting up')
ctrl_pin.value(rx_pin_value)
time.sleep_ms(500)

data_received = False

buff = bytearray(100)
def routine_1():

    print('Waiting for input...')
    while True:
        # initialise receive mode
        ctrl_pin.value(rx_pin_value)

        data_avail = uart.any()  # Gets number of characters which can be read from UART

        if data_avail > 0 and sum(buff) > 0:

            print(f'Data received! Characters: {data_avail}')
            uart.readinto(buff)
            print(buff)

            time.sleep_ms(111)
            # initialise send / reply mode
            print('Sending reply')
            ctrl_pin.value(tx_pin_value)
            uart.write(b'ok --> ')
            uart.write(buff[0:data_avail])

            buff[:] = b'\x00' * len(buff)

        time.sleep_ms(1000)

def constant_broadcast(frequency_hz, pause_every):
    # emits a message on a regular basis
    count = 0
    print(f'Starting periodic broadcast with frequency {frequency_hz}')
    while True:
        ctrl_pin.value(tx_pin_value)
        print(f'Sending message number: {count}')
        uart.write(bytearray(f'Message number:{count}'))

        count += 1
        time.sleep(1 / frequency_hz)
        if count % pause_every == 0:
            time.sleep(20)

if __name__ == '__main__':
    constant_broadcast(1, 10)