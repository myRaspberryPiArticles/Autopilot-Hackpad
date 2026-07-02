# encoder.py
import rotaryio
import board
from adafruit_hid.keycode import Keycode
import time

# 1. Initialize all three hardware encoders
encoder_alt = rotaryio.IncrementalEncoder(board.GP13, board.GP12)
encoder_head = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
encoder_speed = rotaryio.IncrementalEncoder(board.GP26, board.GP27)

# 2. Persistent Tracking Variables
heading_val = 360  
last_position_head = None

speed_val = 200  
last_position_speed = None

alt_val = 10000
last_position_alt = None

def check_alt_encoder(kbd):
    global last_position_alt, alt_val
    alt_pos = encoder_alt.position
    
    if last_position_alt is None:
        last_position_alt = alt_pos
        return None
        
    if alt_pos != last_position_alt:
        raw_steps = alt_pos - last_position_alt
        steps = -raw_steps  
        
        if steps > 0:
            for _ in range(steps):
                kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.E)
                time.sleep(0.040)  # Hold time for MSFS
                kbd.release_all()
                time.sleep(0.025)  # INTERMISSION: Let the sim process it
            alt_val += (steps * 100)  
            
        elif steps < 0:
            for _ in range(abs(steps)):
                kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.W)
                time.sleep(0.040)
                kbd.release_all()
                time.sleep(0.025)
            alt_val += (steps * 100)  
            
        if alt_val < 0:
            alt_val = 0
            
        last_position_alt = alt_pos
        return f"ALT: {alt_val:05d}"
        
    return None


def check_head_encoder(kbd):
    global last_position_head, heading_val
    head_pos = encoder_head.position
    
    if last_position_head is None:
        last_position_head = head_pos
        return None
        
    if head_pos != last_position_head:
        raw_steps = head_pos - last_position_head
        steps = -raw_steps  
        
        if steps > 0:
            for _ in range(steps):
                kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.P)
                time.sleep(0.040)
                kbd.release_all()
                time.sleep(0.025)
            heading_val += steps  
            
        elif steps < 0:
            for _ in range(abs(steps)):
                kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.L)
                time.sleep(0.040)
                kbd.release_all()
                time.sleep(0.025)
            heading_val += steps  
            
        if heading_val > 360:
            heading_val = 0
        elif heading_val < 0:
            heading_val = 360
            
        last_position_head = head_pos
        return f"HDG: {heading_val:03d}"
        
    return None


def check_speed_encoder(kbd):
    global last_position_speed, speed_val
    speed_pos = encoder_speed.position
    
    if last_position_speed is None:
        last_position_speed = speed_pos
        return None
        
    if speed_pos != last_position_speed:
        raw_steps = speed_pos - last_position_speed
        steps = -raw_steps  
        
        if steps > 0:
            for _ in range(steps):
                kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.Z)
                time.sleep(0.040)
                kbd.release_all()
                time.sleep(0.025)
            speed_val += steps  
            
        elif steps < 0:
            for _ in range(abs(steps)):
                kbd.press(Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.Q)
                time.sleep(0.040)
                kbd.release_all()
                time.sleep(0.025)
            speed_val += steps  
            
        if speed_val < 0:
            speed_val = 0
            
        last_position_speed = speed_pos
        return f"SPD: {speed_val:03d}"
        
    return None
