#import the library to control the GPIO pins
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#import the time library
import time

not_oe = 8
le = 10
clk = 12
sdo = 16

#set the pin to be an output
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

digits = [
 [ 1,1,1,1,1,1,0 ], # 0
 [ 0,1,1,0,0,0,0 ], # 1
 [ 1,1,0,1,1,0,1 ], # 2
 [ 1,1,1,1,0,0,1 ], # 3
 [ 0,1,1,0,0,1,1 ], # 4
 [ 1,0,1,1,0,1,1 ], # 5
 [ 0,0,1,1,1,1,1 ], # 6
 [ 1,1,1,0,0,0,0 ], # 7
 [ 1,1,1,1,1,1,1 ], # 8
 [ 1,1,1,0,0,1,1 ], # 9
]
digits = [
 [ 1,0,0,0,0,0,0,0 ], # 0
 [ 0,1,0,0,0,0,0,0 ], # 0
 [ 0,0,1,0,0,0,0,0 ], # 0
 [ 0,0,0,1,0,0,0,0 ], # 0
 [ 0,0,0,0,1,0,0,0 ], # 0
 [ 0,0,0,0,0,1,0,0 ], # 0
 [ 0,0,0,0,0,0,1,0 ], # 0
 [ 0,0,0,0,0,0,0,1 ], # 0
]
def send_digit(digit,point=False):
    GPIO.output(not_oe, True)

    print("sending:", digits[digit])

    #next 7 clock pulses
    for i in range(8):
        GPIO.output(clk,False)
#        time.sleep(0.01)
        #data
        if digits[digit][i]:
            GPIO.output(sdo,True)
        else:
            GPIO.output(sdo,False)

        GPIO.output(clk,True)
#        time.sleep(0.01)


    GPIO.output(clk,True)
#    time.sleep(0.01)

    #latch
    GPIO.output(le,True)
#    time.sleep(0.01)
    GPIO.output(le,False)

    #turn on leds
    GPIO.output(not_oe, False)

while True:
    for i in range(8):
        send_digit(i,False)
        time.sleep(0.1)
