import RPi.GPIO as GPIO
import time
from models.parking import Parking

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = [17,6,16]
GPIO_ECHO = [18,12,13]
GPIO_LED = [4,5,26]
LED1 = 27
LED2 = 22
LED3 = 23

GPIO.setup(LED1, GPIO.OUT, initial=1)
GPIO.setup(LED2, GPIO.OUT, initial=1)
GPIO.setup(LED3, GPIO.OUT, initial=1)

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

def index_to_id(i):
    id = i
    
    if i == 0:
        id = 1
    elif i == 1:
        id = 5
    elif i == 2:
        id = 7
    
    return id + 1

def run():
    try:
        # During the first run, update prev_status, status and DB correctly
        # based on the sensor status
        print("Starting...")
        prev_status = [False, False, False]
        status = [False, False, False]
        for i in range(3):
            distance = ping(GPIO_TRIGGER[i], GPIO_ECHO[i])
            if distance <= 7:
                GPIO.output(GPIO_LED[i], 1)
                prev_status[i] = True
                status[i] = True
                query = Parking.update(status = True).where(Parking.id == index_to_id(i)) 
                query.execute()
            else:
                GPIO.output(GPIO_LED[i], 0)
                prev_status[i] = False
                status[i] = False
                query = Parking.update(status = False).where(Parking.id == index_to_id(i)) 
                query.execute()       
        
        # Subsequently, only update DB if the status changes
        while True:
            for i in range(3):
                distance = ping(GPIO_TRIGGER[i], GPIO_ECHO[i])
                if distance <= 7:
                    GPIO.output(GPIO_LED[i], 1)
                    status[i] = True
                else:
                    GPIO.output(GPIO_LED[i], 0)
                    status[i] = False
            
            print('previous status: ', prev_status)
            print('current status: ', status)
            for index, ps in enumerate(prev_status):
                if status[index] != ps:
                    query = Parking.update(status = status[index]).where(Parking.id == index_to_id(index))
                    query.execute()
            
            prev_status = status.copy()
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Program Stopped")
        GPIO.cleanup()
