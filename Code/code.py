import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_ssd1306
import neopixel
import busio
import time
from encoder import *
from switch import *

WIDTH = 128
HEIGHT = 64

PIXEL_PIN = board.GP7   # Data In pin
NUM_PIXELS = 5          # 5 total NeoPixels

# Set auto_write=False to manage data transmission smoothly
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False)

# Clear all pixels at boot
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(0.5)

# Bitbang I2C setup for OLED stability
my2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, my2c)
kbd = Keyboard(usb_hid.devices)

# Button Pins
speed_button = digitalio.DigitalInOut(board.GP3)
heading_button = digitalio.DigitalInOut(board.GP4)
altitude_button = digitalio.DigitalInOut(board.GP5)
cmd_a_button = digitalio.DigitalInOut(board.GP29)
cmd_b_button = digitalio.DigitalInOut(board.GP2)
cabin_call_button = digitalio.DigitalInOut(board.GP6)

def setup_btns(button):
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

setup_btns(speed_button)
setup_btns(heading_button)
setup_btns(altitude_button)
setup_btns(cmd_a_button)
setup_btns(cmd_b_button)
setup_btns(cabin_call_button)

# --- TOGGLE TRACKING VARIABLES ---
speed_active = False
heading_active = False
altitude_active = False
cmd_a_active = False
cmd_b_active = False
cabin_active = False

last_speed_btn = True
last_heading_btn = True
last_altitude_btn = True
last_cmd_a_btn = True
last_cmd_b_btn = True
last_cabin_btn = True

# Assuming your switch is on pin GP16
at_arm_switch = digitalio.DigitalInOut(board.GP16)
at_arm_switch.direction = digitalio.Direction.INPUT
at_arm_switch.pull = digitalio.Pull.UP

last_switch_state = True  

# --- NON-BLOCKING SCREEN CLEAR VARIABLES ---
last_display_time = 0.0   # Stores the timestamp of the last screen update
screen_is_active = True   # Tracks if there is text currently visible on screen
CLEAR_DELAY = 3.0         # Time in seconds before turning off the screen text

while True:
    update_oled = False
    current_msg = ""
    
    # Read all button physical values right now
    speed_val = speed_button.value
    heading_val = heading_button.value
    altitude_val = altitude_button.value
    cmd_a_val = cmd_a_button.value
    cmd_b_val = cmd_b_button.value
    cabin_val = cabin_call_button.value

    # --- Button 1: SPEED -> Pixel 0 ---
    if speed_val == 0 and last_speed_btn == True:
        speed_active = not speed_active  
        kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.J)
        current_msg = "IAS/MACH"
        update_oled = True
    
    pixels[0] = (0, 255, 0) if speed_active else (0, 0, 0)
    kbd.release(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.J)
    last_speed_btn = speed_val  

    # --- Button 2: HEADING -> Pixel 1 ---
    if heading_val == 0 and last_heading_btn == True:
        heading_active = not heading_active
        kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.H)
        current_msg = "HEADING"
        update_oled = True
        
    pixels[1] = (0, 255, 0) if heading_active else (0, 0, 0)
    kbd.release(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.H)
    last_heading_btn = heading_val

    # --- Button 3: ALTITUDE -> Pixel 2 ---
    if altitude_val == 0 and last_altitude_btn == True:
        altitude_active = not altitude_active
        kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.D)
        current_msg = "ALTITUDE"
        update_oled = True
        
    pixels[2] = (0, 255, 0) if altitude_active else (0, 0, 0)
    kbd.release(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.D)
    last_altitude_btn = altitude_val
    
    # --- Button 4: CMD A -> Pixel 4 --- 
    if cmd_a_val == 0 and last_cmd_a_btn == True:
        # IF BOTH ARE OFF: Turn them both ON
        if not cmd_a_active and not cmd_b_active:
            cmd_a_active = True
            cmd_b_active = True
            kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.A)
            time.sleep(0.02)  # Tiny gap so the sim can catch both individual strokes
            kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.B)
        else:
            # OTHERWISE: Turn just CMD A OFF individually
            cmd_a_active = False
            kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.A)
            
        current_msg = "CMD A"
        update_oled = True
    last_cmd_a_btn = cmd_a_val

    # --- Button 5: CMD B -> Pixel 3 ---
    if cmd_b_val == 0 and last_cmd_b_btn == True:
        # IF BOTH ARE OFF: Turn them both ON
        if not cmd_a_active and not cmd_b_active:
            cmd_a_active = True
            cmd_b_active = True
            kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.A)
            time.sleep(0.02)
            kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.B)
        else:
            # OTHERWISE: Turn just CMD B OFF individually
            cmd_b_active = False
            kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.B)
            
        current_msg = "CMD B"
        update_oled = True
    last_cmd_b_btn = cmd_b_val

    # Global LED Update
    pixels[4] = (0, 255, 0) if cmd_a_active else (0, 0, 0)
    pixels[3] = (0, 255, 0) if cmd_b_active else (0, 0, 0)

    # --- Button 6: CABIN CALL ---
    if cabin_val == 0 and last_cabin_btn == True:
        cabin_active = not cabin_active
        kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.C)
        current_msg = "CABIN CALL"
        update_oled = True
        
    last_cabin_btn = cabin_val
        
    # --- Encoders & Switches Processing ---
    alt_changed = check_alt_encoder(kbd)
    head_changed = check_head_encoder(kbd)
    speed_changed = check_speed_encoder(kbd)
    switch_msg = check_toggle_switch(kbd)
    
    if alt_changed:
        current_msg = alt_changed  
        update_oled = True
    elif head_changed:
        current_msg = head_changed  
        update_oled = True
    elif speed_changed:
        current_msg = speed_changed  
        update_oled = True
    elif switch_msg:
        current_msg = switch_msg
        update_oled = True
        
    # Push the color updates out to the NeoPixels physical hardware
    pixels.show()

    # --- RENDER STRATEGY ---
    # Update OLED if a value changed
    if update_oled:
        oled.fill(0)
        oled.text(current_msg, 10, 35, 1, size=2)
        oled.show()
        last_display_time = time.monotonic()  # Log the exact time text was drawn
        screen_is_active = True

    # Check if the delay window has passed to clear the screen without pausing
    if screen_is_active and (time.monotonic() - last_display_time >= CLEAR_DELAY):
        oled.fill(0)
        oled.show()
        screen_is_active = False  # Mark screen as blank so we stop running oled.show() needlessly

    time.sleep(0.01)  # Snappy, uniform 10ms loop debounce gap
