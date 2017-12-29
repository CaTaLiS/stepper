import numpy
import time

class StepperMotor:
    
    motor_methods = ['wave_drive', 'full_step', 'half_step']
    
    def __init__(self, orange_pin, yellow_pin, pink_pin, blue_pin, gpio_wrapper, motor_method='wave_drive'):
        self.__orange_pin = orange_pin
        self.__yellow_pin = yellow_pin
        self.__pink_pin = pink_pin
        self.__blue_pin = blue_pin
        
        self.__gpio = gpio_wrapper
        self.__gpio.prepare_pins([orange_pin, yellow_pin, pink_pin, blue_pin])
        
        self.set_motor_method(motor_method)
        
    def set_step(self, pink_state, orange_state, blue_state, yellow_state):
        self.__gpio.output(self.__pink_pin, pink_state)
        self.__gpio.output(self.__orange_pin, orange_state)
        self.__gpio.output(self.__blue_pin, blue_state)
        self.__gpio.output(self.__yellow_pin, yellow_state)
        
    def forward(self, delay=2, steps=512):
        print('Moving forward {} steps with {} ms of delay...'.format(steps, delay))
        for i in range(steps):
            for j in range(self.step_count):
                self.set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(delay/1000.0)
        self.set_step(0, 0, 0, 0)
                
    def backwards(self, delay=2, steps=512):
        print('Moving backwards {} steps with {} ms of delay...'.format(steps, delay))
        for i in range(steps):
            for j in reversed(range(self.step_count)):
                self.set_step(self.seq[j][0], self.seq[j][1], self.seq[j][2], self.seq[j][3])
                time.sleep(delay/1000.0)
        self.set_step(0, 0, 0, 0)
    
    def set_motor_method(self, method):
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
            self.seq[0] = [1,0,1,0]
            self.seq[1] = [1,0,0,1]
            self.seq[2] = [0,1,0,1]
            self.seq[3] = [0,1,1,0]
        elif method == 'half_step':
            self.step_count = 8
            self.seq = numpy.zeros(shape=(8,4))
            self.seq[0] = [0,0,1,0]
            self.seq[1] = [1,0,1,0]
            self.seq[2] = [1,0,0,0]
            self.seq[3] = [1,0,0,1]
            self.seq[4] = [0,0,0,1]
            self.seq[5] = [0,1,0,1]
            self.seq[6] = [0,1,0,0]
            self.seq[7] = [0,1,1,0]
        else:
            raise ValueError('{} motor method is unsupported!'.format(method))
        