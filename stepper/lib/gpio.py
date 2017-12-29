import RPi.GPIO as GPIO

class GPIOWrapper:
    
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
    def prepare_pins(self, pins_list):
        for pin in pins_list:
            GPIO.setup(pin, GPIO.OUT)

    def output(self, pin_number, state):
        GPIO.output(int(pin_number), int(state))