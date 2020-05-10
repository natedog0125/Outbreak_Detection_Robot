#container for board base pin names
import board
#module contains classes to support a variety of serial protocols.
import busio
#module contains classes to provide access to analog IO typically
#implemented with digital-to-analog (DAC) and analog-to-digital (ADC) converters
import analogio
#module contains classes to provide access to basic digital IO
import digitalio
#module is a strict subset of the CicuitPython time module
import time
#radio tranmitter library
import adafruit_rfm69


#digital value frequency of the radio in Mhz
RADIO_FREQ_MHZ = 915.0

#designate the chip select and reset pins
CS = digitalio.DigitalInOut(board.D4)
RESET = digitalio.DigitalInOut(board.D2)

#initialize SPI bus.
spi = busio.SPI(board.D13, MOSI=board.D11, MISO=board.D12)

#initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

#optionally set an encryption key (16 byte AES key). MUST match both
#on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

#designate the pin that takes input from the gas sensor
gasPin = analogio.AnalogIn(board.A0)

#loop
x=1
while x==1:
    #send a blank message
    rfm69.send(bytes('\r\n',"utf-8"))
    #if gas value is under threshold
    if gasPin.value < 60000:
        #set variable equal to the value of the gasPin
        gasVal = gasPin.value
        print(gasVal)
        #send the current value
        rfm69.send(bytes('{0}'.format(gasVal),"utf-8"))
        #delay for 1 second
        time.sleep(1)

    #if gas value is over threshold
    elif gasPin.value > 60000:
        #send warning to user
        rfm69.send(bytes('HAZARDOUS!\r\n',"utf-8"))
        print(warning)
        #delay for 1 second
        time.sleep(1)