import RPi.GPIO as GPIO
import numpy

class GPIOWrapper:
    
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
    def prepare_pins(self, pins_list):
        for pin in pins_list:
            GPIO.setup(pin, GPIO.OUT)

    def output(self, pin_number, state):
        GPIO.output(int(pin_number), int(state))

import time

class StepperMotor:
    
    methods = {'wave_drive', 'full_step', 'half_step'}
    
    def __init__(self, orange_pin, yellow_pin, pink_pin, blue_pin, gpio_wrapper):
        self.__orange_pin = orange_pin
        self.__yellow_pin = yellow_pin
        self.__pink_pin = pink_pin
        self.__blue_pin = blue_pin
        self.__gpio = gpio_wrapper
        self.__gpio.prepare_pins([orange_pin, yellow_pin, pink_pin, blue_pin])
        self.set_method('half_step')
        
    def set_step(self, pink_state, orange_state, blue_state, yellow_state):
        self.__gpio.output(self.__pink_pin, pink_state)
        self.__gpio.output(self.__orange_pin, orange_state)
        self.__gpio.output(self.__blue_pin, blue_state)
        self.__gpio.output(self.__yellow_pin, yellow_state)
        
    def forward(self, delay=2, steps=512):
        for i in range(steps):
            for j in range(self.step_count):
                self.set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(delay)
    
    def set_method(self, method):
        if method == 'wave_drive':
            self.step_count = 4
            self.seq = numpy.zeros(shape=(4,4))
            self.seq[0] = [0,0,1,0]
            self.seq[1] = [1,0,0,0]
            self.seq[2] = [0,0,0,1]
            self.seq[3] = [0,1,0,0]
        elif method == 'full_step':
            self.step_count = 4
            self.seq = numpy.zeros(shape=(4,4))
            #p,o,b,y
            self.seq[0] = [1,0,1,0]
            self.seq[1] = [1,0,0,1]
            self.seq[2] = [0,1,0,1]
            self.seq[3] = [0,1,1,0]
        elif method == 'half_step':
            self.step_count = 8
            self.seq = numpy.zeros(shape=(8,4))
            #p,o,b,y
            self.seq[0] = [0,0,1,0]
            self.seq[1] = [1,0,1,0]
            self.seq[2] = [1,0,0,0]
            self.seq[3] = [1,0,0,1]
            self.seq[4] = [0,0,0,1]
            self.seq[5] = [0,1,0,1]
            self.seq[6] = [0,1,0,0]
            self.seq[7] = [0,1,1,0]
        else:
            pass

if __name__ == '__main__':
    print('Starting stepper app...')
    
    gpio = GPIOWrapper()
    motor = StepperMotor(4, 17, 27, 22, gpio)
    
    delay = raw_input("Time Delay (ms)?")
    steps = raw_input("How many steps forward? ")
    motor.forward(int(delay) / 1000.0, int(steps))
