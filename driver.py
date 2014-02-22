"""
title: big 7 segment driver
author: matt venn, 2014
license: GPL attribution share alike
"""
import time

#verbose output
verbose = True

#how long to wait before next char sent
scroll_time = 1.0
BLANK = 10

#undefine for testing with GPIO lib
raspi = True

if raspi:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

#pin defs
not_oe = 8 #output enable
le = 10 #latch
clk = 12 #clock
sdo = 16 #data out

#set the pins to be outputs
if raspi:
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

#sends a string representation of a float, deals with floating points
def update(number,scroll=False):
    #turn leds off before update
#    turn_off()
    point = False
    
    if scroll:
        for char in number:
            if char == '.':
                send_digit(BLANK,True)
            else:
                send_digit(int(char),False)

            #latch the outputs
            if raspi:
                GPIO.output(le,True)
                GPIO.output(le,False)

            time.sleep(scroll_time)

    else:
        #send least significant digit first
        for char in reversed(number):
            if char == '.':
                point = True
                continue
            send_digit(int(char),point)
            point = False

        #latch the outputs
        if raspi:
            GPIO.output(le,True)
            GPIO.output(le,False)
    
    #turn on leds
#    turn_on()

#send a number, with optional point
def send_digit(digit,point=False):
    #set the point bit
    if point:
        digits[digit][7] = 1
    else:
        digits[digit][7] = 0

    if verbose:
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
def turn_off():
    if raspi:
        GPIO.output(not_oe, True)

#turn on leds
def turn_on():
    if raspi:
        GPIO.output(not_oe, False)

def init_pwm():
    p = GPIO.PWM(not_oe, 50)
    p.start(1)
    return p

def set_pwm(p,pwm):
    p.ChangeDutyCycle(pwm)

#run a test sequence
if __name__ == '__main__':
    print("running test sequence")
    point = False
#    turn_on()
    p = init_pwm()
    set_pwm(p,50)
    while True:
        for i in range(100):
            print("sending %.1f" % (i/10.0))
            time.sleep(0.10)
            update("%02d" % (i))
