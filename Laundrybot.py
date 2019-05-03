import RPi.GPIO as GPIO
import time
from pushbullet import Pushbullet
from gpiozero import Button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
from datetime import datetime

#GPIO Setup
sens_pin = 2
button_pin = 16
led_pin = 26
GPIO.setup(sens_pin, GPIO.IN) #SensPin Setup
GPIO.setup(button_pin, GPIO.OUT) #ButtonPinSetup
GPIO.setup(led_pin, GPIO.OUT) #LEDPin Out

#PushBullet Setup
pb = Pushbullet("o.lOs7ZwuENh32HkP7kZ0lhmjW6Rf0E2Bf")

#
# Functions & Variables
#

button = Button(button_pin)
trigg = 0
i = 0
logs = [None] * 5
val = 1
print("Program Started")

def servicecleanup():
        GPIO.output(led_pin, GPIO.LOW)
        i = 0
        trigg = 0
def pushJobDone():
        pb.push_note("Laundry Bot", "Beep Bloop! The Laundry is Done!" )
def pushJobStart():
        pb.push_note("Laundry Bot", "I Will Watch over your Laundry like Batman Watches Gotham City")

def check(logs, val):
        return(all(x < val for x in logs))


#
#CODE
#

while (True): #MasterLoop
        print("Service Re/Started")
        button.wait_for_press()
        pushJobStart()
        logs.clear()
        trigg = 0
        logs = [None] * 5 # PURGE LOGS
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(5) #CHANGE THIS VALUE TO 200 IN PROD
        GPIO.output(led_pin, GPIO.LOW)

        while( i < 7200 and trigg == 0): #ActiveLoop
                if GPIO.input(sens_pin): #Writing To Monitoring Log
                        logs.pop(0)
                        logs.append(1)
                        print(logs)
                if GPIO.input(sens_pin) == 0:
                        logs.pop(0)
                        logs.append(0)
                        print(logs)

                if i > 20:
                        if (check(logs,val)):
                                trigg = 1
                                pushJobDone()
                                print("Job Is Done! Bailing Out of Monitoring Process")
                if (i > 7199):
                        print ("TIMEOUT. TRIGGERING BAILOUT")
                        trigg = 1
                        pb.push_note("Laundry Bot" , "UH OH! Something went wrong. Monitoring Service Cancelled!")

                i += 1
                time.sleep(1)
