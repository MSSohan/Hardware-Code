from PIL import Image, ImageDraw, ImageFont
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
from time import sleep
import time
import requests as rq
import os
import time
import cups

# Raspberry Pi configuration.
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0
BORDER = 7
BORDER2 = 3
WIDTH = 240
HEIGHT = 320

#CUPS Connections
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = list(printers.keys())[0]

#Connect Host IP Adress
host = 'http://192.168.0.120:5000/'

disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

class keypad():
    # CONSTANTS
    KEYPAD = [
        [1,   2,   3],
        [4,   5,   6],
        [7,   8,   9],
        ["*", 0, "#"]
    ]

    COLUMN      = [4,17,22]
    ROW         = [27,12,24,25]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def getKey(self):
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return

        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 3.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j

        # if colVal is not 0 thru 3 then no button was pressed and we can exit
        if colVal < 0 or colVal > 3:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]

    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
    # Initialize the keypad class
    kp = keypad()
def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r

while True:
    disp.clear((0, 0, 255))
    if 1==1:
        # Initialize display.
        disp.begin()
        # Clear the display to a red background
        disp.clear((0, 0, 255))
        # Get a PIL Draw object to start drawing on the display buffer.
        draw = disp.draw()
        draw.rectangle((BORDER2, BORDER2, WIDTH - BORDER2 - 1, HEIGHT - BORDER2 - 1), fill=(0,100,255))
        draw.rectangle((BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1), fill=(0,180,150))
        # Load default font.
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 35)
        font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        def draw_rotated_text(image, text, position, angle, font, fill=(0,0,0)):
            # Get rendered font width and height.
            draw = ImageDraw.Draw(image)
            width, height = draw.textsize(text, font=font)
            # Create a new image with transparent background to store the text.
            textimage = Image.new('RGBA', (width, height), (0,0,0,0))
            # Render the text.
            textdraw = ImageDraw.Draw(textimage)
            textdraw.text((0,0), text, font=font, fill=fill)
            # Rotate the text image.
            rotated = textimage.rotate(angle, expand=1)
            # Paste the text into the image, using it as a mask for transparency.
            image.paste(rotated, position, rotated)
            
        if 1==1:
            draw_rotated_text(disp.buffer,"Welcome To ", (35, 45), 90, font, fill=(0,0,255))
            disp.display()
            sleep(1)
            
            if 1==1:
                draw_rotated_text(disp.buffer,"Cloud Printing ", (70, 10), 90, font2, fill=(255,0,0))
                disp.display()
                sleep(1)
                
                if 1==1:
                    draw_rotated_text(disp.buffer,"Service", (110, 80), 90, font3, fill=(0,0,200))
                    disp.display()
                    sleep(2)
                    disp.clear()
                    
                    try:
                        response = rq.get(host+'doc_to_print').json()                        
                        if 1==1:
                            disp.clear((0, 0, 255))
                            draw = disp.draw()
                            draw.rectangle((BORDER2, BORDER2, WIDTH - BORDER2 - 1, HEIGHT - BORDER2 - 1), fill=(0,100,255))
                            draw.rectangle((BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1), fill=(0,180,150))
                            draw.rectangle((199,7,232,312), fill=(0,60,94))
                            draw.rectangle((110,77,160,240), fill=(0,60,94))
                            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)
                            font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                            font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                    
                            def draw_rotated_text(image, text, position, angle, font, fill=(0,0,0)):
                                draw = ImageDraw.Draw(image)
                                width, height = draw.textsize(text, font=font)
                                textimage = Image.new('RGBA', (width, height), (0,0,0,0))
                                textdraw = ImageDraw.Draw(textimage)
                                textdraw.text((0,0), text, font=font, fill=fill)
                                rotated = textimage.rotate(angle, expand=1)
                                image.paste(rotated, position, rotated)
                                
                            draw_rotated_text(disp.buffer, "Cloud Printing Service", (20, 15), 90, font, fill=(0,0,200))    
                            draw_rotated_text(disp.buffer, "Enter Your OTP", (55, 25), 90, font2, fill=(255,0,0))
                            draw_rotated_text(disp.buffer, "Press * to submit the OTP", (204, 15), 90, font3, fill=(200,200,200))
                            disp.display()
                            
                            d1 = digit()
                            sleep(0.2)
                            draw_rotated_text(disp.buffer, "%s"%(d1), (118, 210), 90, font2, fill=(200,200,200))
                            disp.display()
                        
                            if d1 >= 0:
                                d2 = digit()
                                draw_rotated_text(disp.buffer, "%s"%(d2), (118, 185), 90, font2, fill=(200,200,200))
                                disp.display()
                                sleep(0.2)
                            
                                if digit() >= 0:
                                    d3 = digit()
                                    draw_rotated_text(disp.buffer, "%s"%(d3), (118, 160), 90, font2, fill=(200,200,200))
                                    disp.display()
                                    sleep(0.2)
                                
                                    if digit() >= 0:
                                        d4 = digit()
                                        draw_rotated_text(disp.buffer, "%s"%(d4), (118, 135), 90, font2, fill=(200,200,200))
                                        disp.display()
                                        sleep(0.2)
                                                    
                                        if digit() >= 0:
                                            d5 = digit()
                                            draw_rotated_text(disp.buffer, "%s"%(d5), (118, 115), 90, font2, fill=(200,200,200))
                                            disp.display()
                                            sleep(0.2)
                                                    
                                            if digit() >= 0:
                                                d6 = digit()
                                                draw_rotated_text(disp.buffer, "%s"%(d6), (118, 90), 90, font2, fill=(200,200,200))
                                                disp.display()
                                                sleep(0.2)
                                                PressOTP = "%s%s%s%s%s%s"%(d1,d2,d3,d4,d5,d6)
                            
                                                if digit() == "*":
                                                    for i in range(len(response)):
                                                        if response[i]['otp'] == PressOTP:
                                                            for data in response:
                                                                src = data['src']
                                                                fileName = str(response[i]['src'])
                                                                splitter = fileName.split('\\')
                                                                dir_locs = '/'.join(splitter[2:-1])
                                                                src = '/'.join(splitter)
                                                                os.makedirs(dir_locs, exist_ok=True)
                                                                file_name = splitter[-1]
                                                                file_url = host + src
                                                                dest = '/'.join(splitter[2:]).replace(' ', '')
                                                                os.system(f"wget '{file_url}' -O '{dest}'")

                                                                # Set Print Options
                                                                print_options = {"copies": str(data['copies'])}
                                                                pages = data['pages']

                                                                if pages != 'all':
                                                                    if pages in ['odd', 'even']:
                                                                        print_options['page-set'] = pages
                                                                    else:
                                                                        print_options['page-ranges'] = pages

                                                            disp.clear((0, 0, 255))
                                                            draw = disp.draw()
                                                            draw.rectangle((BORDER2, BORDER2, WIDTH - BORDER2 - 1, HEIGHT - BORDER2 - 1), fill=(0,100,255))
                                                            draw.rectangle((BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1), fill=(0,180,150))
                                                            draw.rectangle((199,7,232,312), fill=(0,60,94))
                                                            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)
                                                            font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
                                                            font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 21)
                                                            font4 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)
                                                            
                                                            def draw_rotated_text(image, text, position, angle, font, fill=(0,0,0)):
                                                                draw = ImageDraw.Draw(image)
                                                                width, height = draw.textsize(text, font=font)
                                                                textimage = Image.new('RGBA', (width, height), (0,0,0,0))
                                                                textdraw = ImageDraw.Draw(textimage)
                                                                textdraw.text((0,0), text, font=font, fill=fill)
                                                                rotated = textimage.rotate(angle, expand=1)
                                                                image.paste(rotated, position, rotated)
                                                                
                                                            draw_rotated_text(disp.buffer, "Cloud Printing Service", (20, 15), 90, font, fill=(0,0,200))
                                                            draw_rotated_text(disp.buffer, "Hi User's_Name", (55, 55), 90, font, fill=(112,0,170))
                                                            draw_rotated_text(disp.buffer, "Printing Details", (88, 50), 90, font2, fill=(255,0,0))
                                                            draw_rotated_text(disp.buffer, "File Name: %s"%(file_name), (117, 62), 90, font3, fill=(15,10,10))
                                                            draw_rotated_text(disp.buffer, "Page Count: %s"%(pages), (145, 86), 90, font3, fill=(15,10,10))
                                                            draw_rotated_text(disp.buffer, "Cost: 25Tk", (172, 108), 90, font3, fill=(15,10,10))
                                                            draw_rotated_text(disp.buffer, "Press * to Continue", (204, 45), 90, font4, fill=(200,200,200))
                                                            disp.display()
                                                            sleep(0.2)
                                                            
                                                            if digit()== "*":
                                                                disp.clear((0, 0, 255))
                                                                draw = disp.draw()
                                                                draw.rectangle((BORDER2, BORDER2, WIDTH - BORDER2 - 1, HEIGHT - BORDER2 - 1), fill=(0,100,255))
                                                                draw.rectangle((BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1), fill=(0,180,150))
                                                                draw.rectangle((180,7,232,312), fill=(0,60,94))
                                                                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)
                                                                font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)
                                                                
                                                                def draw_rotated_text(image, text, position, angle, font, fill=(0,0,0)):
                                                                    draw = ImageDraw.Draw(image)
                                                                    width, height = draw.textsize(text, font=font)
                                                                    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
                                                                    textdraw = ImageDraw.Draw(textimage)
                                                                    textdraw.text((0,0), text, font=font, fill=fill)
                                                                    rotated = textimage.rotate(angle, expand=1)
                                                                    image.paste(rotated, position, rotated)
                                                                    
                                                                draw_rotated_text(disp.buffer, "Cloud Printing Service", (20, 15), 90, font, fill=(0,0,200))
                                                                draw_rotated_text(disp.buffer, "Hi User's_Name", (55, 55), 90, font, fill=(112,0,170))
                                                                draw_rotated_text(disp.buffer, "Ready To Print", (110, 65), 90, font, fill=(15,10,10))
                                                                draw_rotated_text(disp.buffer, "Press * to Continue", (182, 40), 90, font2, fill=(200,200,200))
                                                                draw_rotated_text(disp.buffer, "Press # to Cancle", (204, 50), 90, font2, fill=(200,200,200))
                                                                disp.display()
                                                                sleep(0.2)
                                                        
                                                                if digit()== "*":
                                                                    disp.clear((0, 0, 255))
                                                                    draw = disp.draw()
                                                                    draw.rectangle((BORDER2, BORDER2, WIDTH - BORDER2 - 1, HEIGHT - BORDER2 - 1), fill=(0,100,255))
                                                                    draw.rectangle((BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1), fill=(0,180,150))
                                                                    draw.rectangle((199,7,232,312), fill=(0,60,94))
                                                                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)
                                                                    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)
                                                                    
                                                                    def draw_rotated_text(image, text, position, angle, font, fill=(0,0,0)):
                                                                        draw = ImageDraw.Draw(image)
                                                                        width, height = draw.textsize(text, font=font)
                                                                        textimage = Image.new('RGBA', (width, height), (0,0,0,0))
                                                                        textdraw = ImageDraw.Draw(textimage)
                                                                        textdraw.text((0,0), text, font=font, fill=fill)
                                                                        rotated = textimage.rotate(angle, expand=1)
                                                                        image.paste(rotated, position, rotated)
                                                                    
                                                                    #Print Command
                                                                    print_id = conn.printFile(
                                                                    printer_name,
                                                                    f'/home/pi/cloud-printer-remake/rpiScript/{dest}',
                                                                    "", print_options)
                                                                        
                                                                    draw_rotated_text(disp.buffer, "Cloud Printing Service", (20, 15), 90, font, fill=(0,0,200))
                                                                    draw_rotated_text(disp.buffer, "Hi User's_Name", (55, 55), 90, font, fill=(112,0,170))
                                                                    draw_rotated_text(disp.buffer, "Print Complete", (110, 65), 90, font, fill=(15,10,10))
                                                                    draw_rotated_text(disp.buffer, "Done", (204, 125), 90, font2, fill=(200,200,200))
                                                                    disp.display()
                                                                    sleep(3)
                                                                    
                                                                    if 1==1:
                                                                        disp.clear((0, 0, 255))
                                                                        draw = disp.draw()
                                                                        draw.rectangle((BORDER2, BORDER2, WIDTH - BORDER2 - 1, HEIGHT - BORDER2 - 1), fill=(0,100,255))
                                                                        draw.rectangle((BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1), fill=(0,180,150))
                                                                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)
                                                                        font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",28)
                                                                        font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",30)

                                                                        def draw_rotated_text(image, text, position, angle, font, fill=(0,0,0)):
                                                                            draw = ImageDraw.Draw(image)
                                                                            width, height = draw.textsize(text, font=font)
                                                                            textimage = Image.new('RGBA', (width, height), (0,0,0,0))
                                                                            textdraw = ImageDraw.Draw(textimage)
                                                                            textdraw.text((0,0), text, font=font, fill=fill)
                                                                            rotated = textimage.rotate(angle, expand=1)
                                                                            image.paste(rotated, position, rotated)
                                                                            
                                                                        draw_rotated_text(disp.buffer, "Cloud Printing Service", (20, 15), 90, font, fill=(0,0,200))
                                                                        draw_rotated_text(disp.buffer, "Thanks for Using ", (85, 16), 90, font2, fill=(112,10,170))
                                                                        draw_rotated_text(disp.buffer, "Our Service ", (120, 50), 90, font3, fill=(60,10,100))
                                                                        disp.display()
                                                                        sleep(3)
                                                                        
                                                                elif digit() == "#" :
                                                                    disp.clear()
                                                        else:
                                                            disp.clear((0, 0, 255))
                                                            draw = disp.draw()
                                                            draw.rectangle((BORDER2, BORDER2, WIDTH - BORDER2 - 1, HEIGHT - BORDER2 - 1), fill=(0,100,255))
                                                            draw.rectangle((BORDER, BORDER, WIDTH - BORDER - 1, HEIGHT - BORDER - 1), fill=(0,180,150))
                                                            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

                                                            def draw_rotated_text(image, text, position, angle, font, fill=(0,0,0)):
                                                                draw = ImageDraw.Draw(image)
                                                                width, height = draw.textsize(text, font=font)
                                                                textimage = Image.new('RGBA', (width, height), (0,0,0,0))
                                                                textdraw = ImageDraw.Draw(textimage)
                                                                textdraw.text((0,0), text, font=font, fill=fill)
                                                                rotated = textimage.rotate(angle, expand=1)
                                                                image.paste(rotated, position, rotated)
                                                                
                                                            draw_rotated_text(disp.buffer, " ##Invalid OTP##", (90, 16), 90, font, fill=(250,0,0))
                                                            disp.display()
                                                            sleep(2)
                                                            disp.clear()

                        else:

                            disp.clear()

                    except Exception as e:
                        print("Error: ", e)

                    time.sleep(5)

