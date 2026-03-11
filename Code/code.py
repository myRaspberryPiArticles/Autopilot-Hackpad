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

# buttons
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
