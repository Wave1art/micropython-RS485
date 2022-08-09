# MicroPython RS485 Examples

This repository contains a few examples, debugging tactics and tricks for getting started with RS485 communications using MicroPython on ESP32. It is based on my own experience of trying to get started with RS485 and modbus on micropython and running into a paucity of information to help me.

Each of the examples requires two micropython boards (ESP32) connected by two max3485 chips and associated wiring. Each folder contains two files for the master and the slave device. 

## The basic circuit layout

The bill of materials required to build these examples is:
- 2x ESP32 development boards
- 2x Max3485 ttl to RS485
- 2x 120 ohm resistors
- breadboard / stripboard and appropriate wires to connect everything together

Examples 1 & 2 below were tested using pure micropython v1.19.1 on Lolin D32 Pro v2.0.0 development boards. 

Both of the development boards were wired identically as per the diagram below. 

![Fritzing diagram showing basic wiring](MicroPython_RS485_Example.png?raw=true)

*Circuit notes*

The positive and ground are not shared - each MAX3485 chip connects to +3.3V and Gnd of the board which drives it only1. 

Since RS485 uses differential voltages it is not necessary to include a common ground between each of the devices. Only the two wires A and B are required. Several resources include wiring diagrams where the ground is common between one or more devices but this is misleading and not required. 

RE and DE pins of the MAX3485 chip are connected together. This is the control pin for the MAX3485 chip. It is high when the device is transmitting data and low when the device is listening for data (receive mode). 

The resistor between A and B is repeated for each of the 'devices'. This is as recommended by the Max3485 datasheet. There are diverging opinions on different forums, however the consensous appears to be:
- resistors are not required for short wire runs, definitely required for cabling over a couple of meters to reduce problems associated with noise
- a resistor should be included for _each_ device on a RS485 bus. 
 


## The examples:
1. Basic transmitter and receiver - useful to ensure the correct wiring and establish basic principles
2. RS485 echo - repeats everything sent by the master

### Example 1 - message receiver
In this example the *slave* device simply broadcasts a message with incrementing count number of a periodic basis. The *Master* device listens for each broadcast and prints the received message to the Serial. 

### Example 2 - message echo
The *Master* device sends a message and then switches to receive mode. The *Slave* device waits for a small amount of time (few milliseconds) and then responds, echoing the original message and up-incrementing a count of messages receieved and echoed.

Note that because of the way the echo works (it doesn't wait to check for a stop bit before returning the buffer) the current example will likely overlap partial messages. The point of this example however was to demonstrate send + receive rather than implementing a real world, fault tolerant, communications protocol.  

## Tricks & useful points learned along the way

### Check the UART <-> MAX3485 wiring

The Tx pin of the MAX3485 chip needs to be connected to UART **RX** and vice versa for the RX -> TX pins. It's easy to forget this resulting in no data transmission between devices. 

### Invert logic levels
Since all devices need to use the same logic levels, if no data is being transmitted try inverting the UART Tx/Rx levels in the UART initialisation.

### Device RS485 wiring
In some rare cases manufacturers may have incorrectly wired the A/B of RS485. This should never happen but worth trying if all else fails connecting a device. 

### MicroPython UART does not implement flush
Since UART is asynchronous data may not have completely sent before python execution continues. Arduino implementations include a flush() command to overcome this problem. There is an [active thread here](https://forum.micropython.org/viewtopic.php?t=5739) on the topic, potentially a feature included in future. To work around the issue I simply introduced substantial timing delays in my final solution code. In my case it did not impact functionality since data throughput for my application over RS485 is quite low. 

A more robust approach is to explicitly check the ESP32's UART_STATUS_REG which contains the status of the UART transmitter as per [this part of the post](https://forum.micropython.org/viewtopic.php?t=5739#p33027).

Documentation [here](https://docs.micropython.org/en/latest/esp32/tutorial/peripheral_access.html) shows how to read and write to specific registers from MicroPython. The ESP32 documentation is [here](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf).

### UART.any() may not be reliable
It seems that `UART.any()` may return a spurious number of characters available to read. This is most likely when a new device is added to the bus, for example when in example 1 when the master (listner) is already running and a slave is connected. In practice this is best dealt with by using a communications protocol like Modbus and discarding junk or corrupted messages. 


## Useful resources relating to RS485
Most of these are not directly related to MicroPython or ESP32 but nonetheless were helpful for me to piece together a working solution.
- [MAX3485 - Manufacturer site](https://www.maximintegrated.com/en/products/interface/transceivers/MAX3485.html#tech-docs)
- [MAX3485 Datasheet](https://datasheets.maximintegrated.com/en/ds/MAX3483-MAX3491.pdf)
- [Arduino example](https://www.mischianti.org/2020/05/11/interface-arduino-esp8266-esp32-rs-485/) - Used as inspiration for wiring and intial example
- [Ideas for debugging RS485](https://www.sealevel.com/support/how-to-program-and-debug-rs-485-networks/)
- [Modbus Tools including CRC algorithm](https://www.modbustools.com/modbus.html#lrc)
