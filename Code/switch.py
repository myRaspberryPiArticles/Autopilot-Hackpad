import board
import digitalio
from adafruit_hid.keycode import Keycode

# Set up the switch hardware
switch = digitalio.DigitalInOut(board.GP28)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Start it off matching the physical switch's default state
previous_value = switch.value 

def check_toggle_switch(kbd):
    global previous_value
    current_value = switch.value
    
    # Check if the switch moved AT ALL
    if current_value != previous_value:
        # It moved! Send the shortcut key combo
        kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.S)
        previous_value = current_value # Update our tracker
        
        # Return a message for the OLED based on where it flipped
        if current_value == 0: # 0 means pulled down/connected to ground
            return "A/T ARM"
        else:
            return "A/T ARM"
            
    return None # Return None if the switch didn't move
