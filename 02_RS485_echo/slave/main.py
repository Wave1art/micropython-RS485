# Slave - load this to the device acting as slave

# Example 2 - RS485 Echo
# In this example the Master device sends a message to the Slave device.
# The master switches to receive mode after a short delay to allow the message to be completely sent
# The Slave device will then replay the received message, adding a count of the total number of messages received and sent

# Running the Example:
# 1) Connect the Slave device to power first
# 2) Connect the Master device to power

from machine import UART, Pin
import time
from micropython import const

# RS485 control
print('Setting up control pin')
ctrl_pin = Pin(33, Pin.OUT)
tx_pin_value = const(1)
rx_pin_value = const(0)
ctrl_pin.value(rx_pin_value)  # Start in receive mode to avoid spurious data when connecting devices

print('Setting up UART connected to MAX3485 chip')
uart = UART(2, 9600, bits=8, parity=None, stop=1, tx=25, rx=32)

# Message Send function
def send_message(message_to_send):
    # sends a message over UART -> RS485
    ctrl_pin.value(tx_pin_value)
    print('Send Data')
    uart.write(message_to_send.encode('ascii'))
    time.sleep_ms(100)  # Short delay to allow message to complete sending
    return 0

# Message receive function

buff = bytearray(50)

def receive_message(timeout_seconds = 30):
    # listens for a message RS485 -> UART

    ctrl_pin.value(rx_pin_value)  # set UART to receive mode
    buff[:] = b'\x00' * len(buff)  # reset the buffer

    poll_time = 200  # time between checking the UART any function

    print('Waiting for response...\n')
    for i in range(int(timeout_seconds * 1000 / poll_time)):

        data_avail = uart.any() # Gets number of characters which can be read from UART

        if data_avail > 0:
            print(f'Characters available to read: {data_avail}')
            uart.readinto(buff)
            return buff[0 : data_avail]

        time.sleep_ms(poll_time)

    # if timeed out
    return '-1 : timed out'


# Run the core example as Slave device

# Short sleep to allow time for everything to settle down before starting tx/rx cycle
time.sleep_ms(500)

print('Starting test - Receive + echo...')
count = 0

while True:
    msg_received = receive_message()
    print(f'message received {msg_received}')

    count += 1
    time.sleep_ms(2000)  # wait before replying
    send_message(f'Received message # {count}: {msg_received}')

    # count += 1
    # print(f'sent: {count}')
    # send_message(f'Message Number: {count}')
    # time.sleep(2)