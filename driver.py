"""
title: big 7 segment driver
author: matt venn, 2014
license: GPL attribution share alike
"""
import time

#undefine for testing with GPIO lib
raspi = True

#define which segments are on/off for each digit
#last element is for the point
digits = [
 [ 1,1,1,1,1,1,0,0 ], # 0
 [ 0,1,1,0,0,0,0,0 ], # 1
 [ 1,1,0,1,1,0,1,0 ], # 2
 [ 1,1,1,1,0,0,1,0 ], # 3
 [ 0,1,1,0,0,1,1,0 ], # 4
 [ 1,0,1,1,0,1,1,0 ], # 5
 [ 0,0,1,1,1,1,1,0 ], # 6
 [ 1,1,1,0,0,0,0,0 ], # 7
 [ 1,1,1,1,1,1,1,0 ], # 8
 [ 1,1,1,0,0,1,1,0 ], # 9
 [ 0,0,0,0,0,0,0,0 ], # all off
]

if raspi:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    #pin defs
    not_oe = 8 #output enable
    le = 10 #latch
    clk = 12 #clock
    sdo = 16 #data out

    GPIO.setup(not_oe, GPIO.OUT)
    GPIO.setup(le, GPIO.OUT)
    GPIO.setup(clk, GPIO.OUT)
    GPIO.setup(sdo, GPIO.OUT)

    #turn off leds
    GPIO.output(not_oe, True)
    #turn off latch
    GPIO.output(le,False)
    #clock starts low
    GPIO.output(clk,False)

class driver:
    BLANK = 10
    def __init__(self):
        #verbose output
        self.verbose = True

        #how long to wait before next char sent
        self.scroll_time = 1.3

        freq = 200 #hz
        self.pwm = GPIO.PWM(not_oe, freq)
        #lights off to start with
        self.pwm.start(100) #duty cycle

    #sends a string representation of a float, deals with floating points
    def update(self,number,scroll=False):
        point = False
        
        if scroll:
            for char in number:
                if char == '.':
                    self.send_digit(driver.BLANK,True)
                else:
                    self.send_digit(int(char),False)

                #latch the outputs
                if raspi:
                    GPIO.output(le,True)
                    GPIO.output(le,False)

                time.sleep(self.scroll_time)

        else:
            #send least significant digit first
            for char in reversed(number):
                if char == '.':
                    point = True
                    continue
                self.send_digit(int(char),point)
                point = False

            #latch the outputs
            if raspi:
                GPIO.output(le,True)
                GPIO.output(le,False)
        

    #send a number, with optional point
    def send_digit(self,digit,point=False):
        #set the point bit
        if point:
            digits[digit][7] = 1
        else:
            digits[digit][7] = 0

        if self.verbose:
            print("sending %d%s = %s" % (
                digit,
                '.' if point else '',
                ','.join(str(x) for x in digits[digit]))
                )

        #8 clock pulses
        if raspi:
            for i in range(8):
                GPIO.output(clk,False)
                #data
                if digits[digit][7-i]:
                    GPIO.output(sdo,True)
                else:
                    GPIO.output(sdo,False)

                GPIO.output(clk,True)

    #turn off leds
    def turn_off(self):
        if raspi:
            self.set_pwm(0)

    #turn on leds
    def turn_on(self):
        if raspi:
            self.set_pwm(100)


    def set_pwm(self,pwm):
        self.pwm.ChangeDutyCycle(100-pwm)

    def fade(self,start,end,length):
        if start > end:
           step = -1
        else:
            step = 1
        for i in range(start,end + step,step):
            time.sleep(float(length) / abs(start-end))
            self.set_pwm(i)

    def cleanup(self):
        self.set_pwm(0)
        GPIO.cleanup()
        #cleanup


#run a test sequence
if __name__ == '__main__':
    driver = driver()
    print("running test sequence")
    point = False
    while True:
        for i in range(100):
            print("sending %.1f" % (i/10.0))
            time.sleep(0.10)
            driver.update("%02d" % (i))
