# micropython-RS485

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

*Circuit notes*

RE and DE pins of the MAX3485 chip are connected together. This is the control pin for the MAX3485 chip. It is high when the device is transmitting data and low when the device is listening for data (receive mode). 

The resistor between A and B is repeated for each of the 'devices'. This is as recommended by the Max3485 datasheet. There are diverging opinions on different forums, however the consensous appears to be:
- resistors are not required for short wire runs, definitely required for cabling over a couple of meters to reduce problems associated with noise
- a resistor should be included for _each_ device on a RS485 bus. 

Since RS485 uses differential voltages it is not necessary to include a common ground between each of the devices. Only the two wires A and B are required. Several resources include wiring diagrams where the ground is common between one or more devices but this is misleading and not required. 


## The examples:
1. Basic transmitter and receiver - useful to ensure the correct wiring and establish 
2. RS485 echo - repeats everything sent by the master

### Example 1 - message receiver
In this example the *slave* device simply broadcasts a message 



## Tricks & useful points learned along the way

### Check the UART <-> MAX3485 wiring

The Tx pin of the MAX3485 chip needs to be connected to UART **RX** and vice versa for the RX -> TX pins. It's easy to forget this resulting in no data transmission between devices. 

### Invert logic levels
Since all devices need to use the same logic levels, if no data is being transmitted try inverting the UART Tx/Rx levels in the UART initialisation.

### Dvice RS485 wiring
In some rare cases manufacturers may have incorrectly wired the A/B of RS485. This should never happen but worth trying if all else fails connecting a device. 

### MicroPython UART does not implement flush
Since UART is asynchronous data may not have completely sent before python execution continues. arduino implementations include a flush() commeand to overcome this problem. There is an active thread here on the topic, potentially a feature included in future. To work around the issue I simply introduced substantial timing delays in my final solution code. In my case it did not impact functionality since data throughput for my application over RS485 is quite low. 

### UART.any() may not be reliable









## Useful resources relating to RS485 and related topics
Most of these are not directly related to MicroPython or ESP32 but nonetheless were helpful for me to piece together a working solution.


