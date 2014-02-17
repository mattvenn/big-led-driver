import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#verbose output
verbose = False

#pin defs
not_oe = 8 #output enable
le = 10 #latch
clk = 12 #clock
sdo = 16 #data out

#set the pins to be outputs
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
]

#do the work
def send_digit(digit,point=False):
    GPIO.output(not_oe, True)

    if point:
        digits[digit][7] = 1
    else:
        digits[digit][7] = 0

    if verbose:
        print("sending:", digit, " = ", digits[digit])

    #next 7 clock pulses
    for i in range(8):
        GPIO.output(clk,False)
        #data
        if digits[digit][7-i]:
            GPIO.output(sdo,True)
        else:
            GPIO.output(sdo,False)

        GPIO.output(clk,True)


    GPIO.output(clk,True)

    #latch
    GPIO.output(le,True)
    GPIO.output(le,False)

    #turn on leds
    GPIO.output(not_oe, False)

def turn_off():
    GPIO.output(not_oe, True)

def turn_on():
    GPIO.output(not_oe, False)

#run a test sequence
if __name__ == '__main__':
    print("running test sequence")
    point = False
    while True:
        for i in range(10):
            print("sending %d%s" % (i, "." if point else ""))
            send_digit(i,point)
            time.sleep(0.25)
        if point:
            point = False
        else:
            point = True
