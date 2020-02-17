import RPi.GPIO as GPIO
import time
from models.parking import Parking

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = [17,6,16]
GPIO_ECHO = [18,12,13]
GPIO_LED = [4,5,26]
#LED1 = 27
#LED2 = 22

#GPIO.setup(LED1, GPIO.OUT, initial=1)
#GPIO.setup(LED2, GPIO.OUT, initial=0)

for i in range (3):
    GPIO.setup(GPIO_TRIGGER[i], GPIO.OUT)
    GPIO.setup(GPIO_ECHO[i], GPIO.IN)
    GPIO.setup(GPIO_LED[i], GPIO.OUT)
    
def led():
    GPIO.output(LED1, not GPIO.input(LED1))
    GPIO.output(LED2, not GPIO.input(LED2))
    time.sleep(0.01)

def ping (TRIGGER, ECHO):
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    
    distance = round((TimeElapsed*34300)/2, 1)
    
    return distance


def run():
    try:
        print("Starting...")
        while True:
            for i in range(3):
                distance = ping(GPIO_TRIGGER[i], GPIO_ECHO[i])
                if distance <= 7:
                    GPIO.output(GPIO_LED[i], 1)
                    if i == 1:
                        i = 6
                    elif i == 2:
                        i = 7
                    query = Parking.update(status = True).where(Parking.id == i+1)
                    query.execute()
                else:
                    GPIO.output(GPIO_LED[i], 0)
                    if i == 1:
                        i = 6
                    elif i == 2:
                        i = 7
                    query = Parking.update(status = False).where(Parking.id == i+1)
                    query.execute()
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Program Stopped")
        GPIO.cleanup()
