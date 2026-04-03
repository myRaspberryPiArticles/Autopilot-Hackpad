# Autopilot-Hackpad
This is my HackPad project for the Hack Club Blueprint YSWS! 
I have designed this to work with my flight simulator to make autopilot configuration easier and more immersive. Before you scroll down, a few important notes! Firstly, as TinkerCAD does not support STEP files, I hav provided STL files and the link to my design, so you can export it int different softwares if you wish! Secondly, note that I will buy and source some of the parts myself, because they are not provided by Hack Club. We have discussed the second point many times on Slack and confirmed that we can do this!

## Features
 - 0.91" OLED display to show autopilot configuration
 - Rotary encoders to set the Heading, Altitiude and Speed of the plane
 - Mechanical keyswitches to toggle settings
 - SK6812s indicate status & selected settings
 - RP2040 Zero (I will pay for this) as it is small and has way over 10 GPIOs - I use 19
 - A HUGE cabin call button that you can spam to make the nice 'ding-dong' sound you hear on a flight!

## Screenshots

PCB view:

<img width="1009" height="719" alt="Screenshot 2026-03-27 at 18 07 34" src="https://github.com/user-attachments/assets/5678b605-5187-4f08-891d-895a41d1be32" />
<img width="1009" height="719" alt="Screenshot 2026-03-27 at 18 07 48" src="https://github.com/user-attachments/assets/f0229094-d6ba-4f37-8cbe-bedabb35dac2" />


Schematic view:
<img width="724" height="612" alt="Screenshot 2026-03-29 at 19 50 50" src="https://github.com/user-attachments/assets/11b8f8d5-1d7c-4785-bc81-dc11e3abdfd6" />

Here are the two parts of the case, the top section and the bottom bumper-style part: You can find my Tinkercad design here: https://www.tinkercad.com/things/kMuqWNtUm2q/edit?returnTo=%2Fthings&sharecode=TvnqmuXe9pAtwGBK2sJ9aHeb2CSNASbWhCyXTYQ4DW4
<img width="544" height="534" alt="Screenshot 2026-03-10 at 19 57 58" src="https://github.com/user-attachments/assets/a3fbb8c1-203f-44be-95fd-9af0ffbd0c7b" />

3D visualization of the PCB
<img width="861" height="623" alt="Screenshot 2026-03-27 at 18 15 13" src="https://github.com/user-attachments/assets/13782da8-6df4-430f-ade6-2b6315496f29" />

3D visualization of the final HackPad - It is my attempt at Fusion360 but you will find the case in the Case folder from Tinkercad

I will assemble it by soldering on all the parts on the top, except the RP2040 Zero which will be upside down, and then snug fit it inside the bottom part of the case. Then, I will put the top part of the case on top and use 4 M3x16mm screws to put it all in place. After that, I might put some sticky rubber spots on the bottom to give it extra grip after it is all in place!

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

Also, when Hack Club comes to printing the case, a baby blue filament would be my preference!
