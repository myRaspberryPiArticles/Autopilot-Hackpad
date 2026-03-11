# Autopilot-Hackpad
This is my HackPad/MacroPad project for the Blueprint YSWS project for Hack Club! I have designed this to work with my MSFS 2024 to make autopilot configuration easier and more immersive. 

## Here are some features and info about what it includes:
 - A small 0.91" OLED display to show the settings you have set
 - 3 EC11 Rotary Encoders to set the Heading, Altitiude and Speed of the plane
 - Some nice mechanical keyswitches for confirmation of what you selected
 - SK6812s to show you waht you selected and if something is triggered or not
 - A RP2040 Zero as it is small and has way over 10 GPIOs for me to use! (I use 19 of them!!!!)
 - A HUGE cabin call button that you can spam as much as you like to make the nice 'ding-dong' sound you hear on a flight!

## Some Screenshots

Here are two of either side of the PCB in KiCad PCB editor:

<img width="904" height="602" alt="Screenshot 2026-03-10 at 19 26 10" src="https://github.com/user-attachments/assets/1649db70-94d2-4820-ab40-c7254cfe39cf" />
<img width="904" height="602" alt="Screenshot 2026-03-10 at 19 26 05" src="https://github.com/user-attachments/assets/6c7fd43e-26d0-41fe-b01d-93663c38cac6" />

This one is the PCB in the schematic view:
<img width="891" height="529" alt="Screenshot 2026-03-11 at 20 01 20" src="https://github.com/user-attachments/assets/5db7afa3-aeb5-4063-8bcf-e498f0990403" />


Here are the two parts of the case, the top section and the bottom bumper-style part:

<img width="544" height="534" alt="Screenshot 2026-03-10 at 19 57 58" src="https://github.com/user-attachments/assets/a3fbb8c1-203f-44be-95fd-9af0ffbd0c7b" />

If you want to see what the board will look like, then here is a 3d visualization:
<img width="865" height="620" alt="Screenshot 2026-03-10 at 20 09 21" src="https://github.com/user-attachments/assets/ad254890-4fe8-4706-856e-666bf3c3936b" />

## A list of parts you will need! (BOM)

5         MX_SK6812MINI-E - LEDs

6         D_DO-35_SOD27_P7.62mm_Horizontal - Diodes

6	        SW_Cherry_MX_1.00u_PCB - Key Switches

1	        SSD1306-0.91-OLED-4pin-128x32 - 0.91" OLED

3        	EC11 Rotary Encoders - Rotary encoders (as said in name)

1	        RP2040-Zero - MCU - RP2040 Zero, chosen for high amout of GPIOs (20+!)

1	        SW_Toggle - One nice toggle switch for master autopilot on/off control

## Code for this MacroPad

Below I have provided some basic testing code for most of the components, and it is written with/in CiruitPython.

```python
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import busio as io
import adafruit_ssd1306
import neopixel

pixel = neopixel.NeoPixel(board.D5, 1, pixel_order=neopixel.GRBW)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
i2c = io.I2C(board.SCL, board.SDA)
kbd = Keyboard(usb_hid.devices)

speed_button = digitalio.DigitalInOut(board.GP3)
altitude_button = digitalio.DigitalInOut(board.GP5)
heading_button = digitalio.DigitalInOut(board.GP4)
cmd_a_button = digitalio.DigitalInOut(board.GP29)
cmd_b_button = digitalio.DigitalInOut(board.GP2)
cabin_call_button = digitalio.DigitalInOut(board.GP6)

def setup_btns(button):
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

setup_btns(speed_button)
setup_btns(altitude_button)
setup_btns(heading_button)
setup_btns(cmd_a_button)
setup_btns(cmd_b_button)
setup_btns(cabin_call_button)

while True:
    
    if speed_button.value == 0:
        kbd.press(Keycode.A)
    elif speed_button.value == 1:
        kbd.release(Keycode.A)

    if altitude_button.value == 0:
        kbd.press(Keycode.B)
    elif altitude_button.value == 1:
        kbd.release(Keycode.B)

    if heading_button.value == 0:
        kbd.press(Keycode.C)
    elif heading_button.value == 1:
        kbd.release(Keycode.C)
    
    if cmd_a_button.value == 0:
        kbd.press(Keycode.D)
    elif cmd_a_button.value == 1:
        kbd.release(Keycode.D)
    
    if cmd_b_button.value == 0:
        kbd.press(Keycode.E)
    elif cmd_b_button.value == 1:
        kbd.release(Keycode.E)

    if cabin_call_button.value == 0:
        kbd.press(Keycode.F)
    elif cabin_call_button.value == 1:
        kbd.release(Keycode.F)

oled.fill(0)
oled.text('Hello', 0, 0)
oled.text('World', 0, 10)
oled.show()

pixel[0] = (0, 255, 0, 0)
```

## Extra Information

There isn't really much else you need to know about this project, but I put this section to share a few small bits of information. 

This includes the fact that the MacroPad was designed to fit cockpits of the 737-MAX in MSFS; and also one smll side note, you will need some glue and M3x16mm screws to put it togehter in the case!
