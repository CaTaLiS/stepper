from lib.gpio import GPIOWrapper
from lib.stepper_motor import StepperMotor
from Tkinter import *

class StepperMotorApp:
    
    gpio = GPIOWrapper()
    motor = StepperMotor(4, 17, 27, 22, gpio)
    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        Label(frame, text='Delay[ms]').grid(row=0, column=0)
        self.delay_value = IntVar()
        Entry(frame, textvariable=self.delay_value).grid(row=0, column=1)
        
        Label(frame, text='Steps').grid(row=1, column=0)
        self.steps_value = IntVar()
        Entry(frame, textvariable=self.steps_value).grid(row=1, column=1)
        
        Label(frame, text='Method').grid(row=2, column=0)
        self.method_list = Listbox(frame, height=1, selectmode=BROWSE)
        for item in self.motor.motor_methods:
            self.method_list.insert(END, item)
        self.method_list.grid(row=2, column=1)
        
        direction_radio_frame = Frame(frame)
        self.forward_direction = BooleanVar()
        forward_select = Radiobutton(direction_radio_frame, text='Forward', variable=self.forward_direction, value=True)
        forward_select.pack(side=LEFT)
        backward_select = Radiobutton(direction_radio_frame,text='Backward', variable=self.forward_direction, value=False)
        backward_select.pack(side=RIGHT)
        direction_radio_frame.grid(row=3, columnspan=2)
        
        button = Button(frame, text='Run', command=self.run)
        button.grid(row=4, columnspan=2)
        
    def run(self):
        selected_motor_method = self.motor.motor_methods[self.method_list.curselection()[0]];
        print('Selected {} method.'.format(selected_motor_method))
        self.motor.set_motor_method(selected_motor_method)
        
        if self.forward_direction.get():
            self.motor.forward(self.delay_value.get(), self.steps_value.get())
        else:
            self.motor.backwards(self.delay_value.get(), self.steps_value.get())

if __name__ == '__main__':
    print('Starting stepper app...')
    root = Tk()
    root.resizable(width=False, height=False)
    root.geometry('600x480')
    root.wm_title('STEPPER MOTOR')
    app = StepperMotorApp(root)
    root.mainloop()
