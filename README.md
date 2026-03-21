# Autopilot-Hackpad
This is my HackPad project for the Hack Club Blueprint YSWS! 
I have designed this to work with my flight simulator to make autopilot configuration easier and more immersive. 

## Features
 - 0.91" OLED display to show autopilot configuration
 - Rotary encoders to set the Heading, Altitiude and Speed of the plane
 - Mechanical keyswitches to toggle settings
 - SK6812s indicate status & selected settings
 - RP2040 Zero (I will pay for this) as it is small and has way over 10 GPIOs - I use 19
 - A HUGE cabin call button that you can spam to make the nice 'ding-dong' sound you hear on a flight!

## Screenshots

PCB view:

<img width="904" height="602" alt="Screenshot 2026-03-10 at 19 26 10" src="https://github.com/user-attachments/assets/1649db70-94d2-4820-ab40-c7254cfe39cf" />
<img width="904" height="602" alt="Screenshot 2026-03-10 at 19 26 05" src="https://github.com/user-attachments/assets/6c7fd43e-26d0-41fe-b01d-93663c38cac6" />

Schematic view:
<img width="891" height="529" alt="Screenshot 2026-03-11 at 20 01 20" src="https://github.com/user-attachments/assets/5db7afa3-aeb5-4063-8bcf-e498f0990403" />


Here are the two parts of the case, the top section and the bottom bumper-style part:
<img width="544" height="534" alt="Screenshot 2026-03-10 at 19 57 58" src="https://github.com/user-attachments/assets/a3fbb8c1-203f-44be-95fd-9af0ffbd0c7b" />

3D visualization of the PCB
<img width="865" height="620" alt="Screenshot 2026-03-10 at 20 09 21" src="https://github.com/user-attachments/assets/ad254890-4fe8-4706-856e-666bf3c3936b" />

3D visualization of the final HackPad - It is my attempt at Fusion360 but you will find the case in the Case folder from Tinkercad
<img width="1299" height="1005" alt="Screenshot 2026-03-21 at 15 06 02" src="https://github.com/user-attachments/assets/98936ebf-bcf3-4760-9a24-f72d538c99b4" />


| Part             | Quantity | Purpose                                    |
|------------------|----------|---------------------------------------------|
| MX_SK6812MINI-E  | 5        | LEDs                                         |
| D_DO-35_SOD27_P7.62mm_Horizontal | 6        | Diodes                                      |
| SW_Cherry_MX_1.00u_PCB | 6        | Key Switches                                 |
| SSD1306-0.91-OLED-4pin-128x32 | 1        | 0.91" OLED Display                            |
| EC11 Rotary Encoders | 3        | Rotary Encoders                               |
| RP2040-Zero       | 1        | MCU (Microcontroller Unit)                    |
| SW_Toggle        | 1        | Toggle Switch (Master Autopilot Control) |


## Code for this MacroPad

Here is an example firmware that you can use for testing. 

The code is written in CircuitPython

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

This includes the fact that the MacroPad was designed to fit cockpits of the 737-MAX in MSFS; and also one small side note, you will need some glue and M3x16mm screws to put it together in the case!
