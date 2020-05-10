#container for board base pin names
import board
#module contains classes to support a variety of serial protocols.
import busio
#module contains classes to provide access to basic digital IO
import digitalio
#motor library
from adafruit_motorkit import MotorKit
#radio tranmitter library
import adafruit_rfm69

#Set Motorkit Library Equal to Kit
kit = MotorKit()

#digital value frequency of the radio in Mhz
RADIO_FREQ_MHZ = 433.0

#designate the chip select and reset pins
CS = digitalio.DigitalInOut(board.D5)
RESET = digitalio.DigitalInOut(board.D6)

#initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
#initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

#optionally set an encryption key (16 byte AES key). MUST match both
#on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

#sets the initial power each motor to off by setting it equal to 0
kit.motor1.throttle = 0
kit.motor2.throttle = 0
kit.motor3.throttle = 0
kit.motor4.throttle = 0

#sets the initial direction of the robot to stop
direction = '0'

#continue loop forever
while True:

    #receive string from controller
    direction_text = rfm69.receive()

    #if the robot receives a direction
    if direction_text is not None:
        direction = str(direction_text, 'ascii')

    #display the the numerical value of the direction that robot is going
    print('move:', direction)

    #the numerical value of each direction:
    #stop = '0'
    #forward = '1'
    #forwardLeft = '5'
    #forwardRight = '8'
    #back = '2'
    #backLeft = '6'
    #backRight = '9'
    #left = '4'
    #right = '7'

    #motors 1 & 4 are the motors on the right side and 2 & 3 are on the left

    #if the direction is in the stop position
    if direction == '0':
        #send no power to the motors
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0

    #if the direction is in the forward position
    elif direction == '1':
        #send max power to the motors
        kit.motor1.throttle = 1
        kit.motor2.throttle = 1
        kit.motor3.throttle = 1
        kit.motor4.throttle = 1

    #if the direction is in the back position
    elif direction == '2':
        #send max power to every motor but in the opposite direction
        kit.motor1.throttle = -1
        kit.motor2.throttle = -1
        kit.motor3.throttle = -1
        kit.motor4.throttle = -1

    #if the direction is in the left position
    elif direction == '4':
        #send max power to the motors on the right
        #but none to the motors on the left
        kit.motor1.throttle = 1
        kit.motor2.throttle = 0
        kit.motor3.throttle = 0
        kit.motor4.throttle = 1

    #if the direction is in the right position
    elif direction == '7':
        #send max power to the motors on the left
        #but none to the motors on the right
        kit.motor1.throttle = 0
        kit.motor2.throttle = 1
        kit.motor3.throttle = 1
        kit.motor4.throttle = 0

    #if the direction is in the forward & left position
    elif direction == '5':
        #send max power to the motors on the right
        #but 3/4 power to the motors on the left
        kit.motor1.throttle = 1
        kit.motor2.throttle = .75
        kit.motor3.throttle = .75
        kit.motor4.throttle = 1

    #if the direction is in the forward & right position
    elif direction == '8':
        #send max power to the motors on the left
        #but 3/4 power to the motors on the right
        kit.motor1.throttle = .75
        kit.motor2.throttle = 1
        kit.motor3.throttle = 1
        kit.motor4.throttle = .75

    #if the direction is in the back & left position
    elif direction == '6':
        #send max power to the motors on the right but in the opposite direction
        #but 3/4 power to the motors on the left but in the opposite direction
        kit.motor1.throttle = -1
        kit.motor2.throttle = -.75
        kit.motor3.throttle = -.75
        kit.motor4.throttle = -1

    #if the direction is in the back & right position
    elif direction == '9':
        #send max power to the motors on the left but in the opposite direction
        #but 3/4 power to the motors on the right but in the opposite direction
        kit.motor1.throttle = -.75
        kit.motor2.throttle = -1
        kit.motor3.throttle = -1
        kit.motor4.throttle = -.75
    else:
        print('Error')