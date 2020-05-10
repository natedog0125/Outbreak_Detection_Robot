#container for board base pin names
import board
#module is a strict subset of the CicuitPython time module
import time
#module contains classes to support a variety of serial protocols.
import busio
#module contains classes to provide access to basic digital IO
import digitalio
#lcd display library
import adafruit_character_lcd.character_lcd as characterlcd
#radio tranmitter library
import adafruit_rfm69


#digital value frequency of the radio in Mhz
RADIO_FREQ_MHZ = 915.0

#designate the chip select and reset pins
CS = digitalio.DigitalInOut(board.D4)
RESET = digitalio.DigitalInOut(board.D3)

# Define the onboard LED
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

#initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

#optionally set an encryption key (16 byte AES key). MUST match both
#on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

print('Waiting for packets...')

#designate the number of characters in width the lcd can display
lcd_columns = 16
#designate the number of lines the lcd can display
lcd_rows = 2

#designate the data pins for the lcd
lcd_rs = digitalio.DigitalInOut(board.D5)
lcd_en = digitalio.DigitalInOut(board.D7)
lcd_d7 = digitalio.DigitalInOut(board.D12)
lcd_d6 = digitalio.DigitalInOut(board.D11)
lcd_d5 = digitalio.DigitalInOut(board.D10)
lcd_d4 = digitalio.DigitalInOut(board.D9)
lcd_backlight = digitalio.DigitalInOut(board.D2)

#function that uses each pin so the lcd will work as a whole, set equal to lcd
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#continue loop forever
while True:
    # Turn backlight on
    lcd.backlight = True
    #receive message from sensors
    packet = rfm69.receive()
    #message to be sent to display
    lcd.message = ""
    if packet is None:
        #if nothing is received the onboard led will be off
        LED.value = False
        print('Received nothing! Listening again...')
    else:
        #if something is received, the onboard led will light up
        LED.value = True
        #translate package as a string
        packet_text = str(packet, 'ascii')
        #send message to display
        lcd.message = ('Gas: {0}'.format(packet_text))