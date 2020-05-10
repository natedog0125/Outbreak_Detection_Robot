#container for board base pin names
import board
#module contains classes to support a variety of serial protocols.
import busio
#module contains classes to provide access to basic digital IO
import digitalio
#module contains classes to provide access to analog IO typically
#implemented with digital-to-analog (DAC) and analog-to-digital (ADC) converters
import analogio
#module is a strict subset of the CicuitPython time module
import time
#module allows you to output data as a HID device
import usb_hid
#radio tranmitter library
import adafruit_rfm69
#module allows you to output data as a HID device,specifically for game controllers
from adafruit_hid.gamepad import Gamepad


#digital value frequency of the radio in Mhz
RADIO_FREQ_MHZ = 433.0

#designate the chip select and reset pins
CS = digitalio.DigitalInOut(board.D4)
RESET = digitalio.DigitalInOut(board.D3)

#initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

#optionally set an encryption key (16 byte AES key). MUST match both
#on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

#set gamepad library equal to gp
gp = Gamepad(usb_hid.devices)

#set 1st joystick equal to xPin
xPin = analogio.AnalogIn(board.A0)
#set 2nd joystick equal to yPin
yPin = analogio.AnalogIn(board.A1)

#mapping function to find ranges
#parameters from beginning to end are as follows:
#x - the device, in_min - x value, in_max - y value,
#out_min - z value, out_max - z rotation value
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

#initial x joystick direction
xDir = 0
#initial y joystick direction
yDir = 0

while True:
    #mapping function to find ranges
    #specifically for the josysticks with their min and max ranges
    gp.move_joysticks(x=range_map(xPin.value, 0, 65535, -127, 127),
                  y=range_map(yPin.value, 0, 65535, -127, 127))

    #if x joystick is in the forward position, set x direction to 1
    if xPin.value > 0 and xPin.value < 500:
        #print('x is up')
        xDir = 1

    #if x joystick is in the back position, set x direction to 2
    elif xPin.value > 30000 and xPin.value < 35000:
        #print('x is down')
        xDir = 2

    #else x joystick is up
    else:
        xDir = 0

    #if y joystick is in the left position, set y direction to 7
    if yPin.value > 30000 and yPin.value < 35000:
        #print('y is left')
        yDir = 7

    #if y joystick is in the right position, set y direction to 4
    elif yPin.value > 0 and yPin.value < 1200:
        #print('y is right')
        yDir = 4

    #else x joystick is up
    else:
        yDir = 0

    #add these directions to be sent to the robot
    #the robot will translate this value as a direction
    #example: x = 1 (forward) & y = 7 (left) which equals 5
    #5 on the robot is translated as forward and left
    sendPin = xDir + yDir
    print(sendPin)
    #send sendPin value to robot (this will be sent as a string)
    rfm69.send(bytes('{0}'.format(sendPin),"utf-8"))
    print(sendPin)