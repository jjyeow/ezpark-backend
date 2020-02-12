#Libraries
import RPi.GPIO as GPIO
import time
from models.parking import Parking

#disable warnings
GPIO.setwarnings(False)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 17
GPIO_ECHO = 18
GPIO_LED = 4

GPIO_TRIGGER2 = 6
GPIO_ECHO2 = 12
GPIO_LED2 = 5

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_LED2, GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    GPIO.output(GPIO_TRIGGER2, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    GPIO.output(GPIO_TRIGGER2, False)

    # set start/stop for each sensor
    StartTime = time.time()
    StopTime = time.time()

    StartTime2 = time.time()
    StopTime2 = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime2 = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime2 = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    TimeElapsed2 = StopTime2 - StartTime2

    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = round((TimeElapsed * 34300) / 2, 1)
    distance2 = round((TimeElapsed2 * 34300) / 2, 1)
 
    return distance, distance2
 
def run():
    # if __name__ == '__main__':
    try:
        while True:
            [dist, dist2] = distance()

            if dist <= 6:
                print ("Measured distance = %.1f cm" % dist)
                time.sleep(0.1)
                GPIO.output(GPIO_LED, 1)
                query = Parking.update(status = True).where(Parking.id == 1) #sensor 1
                query.execute()
            else:
                print ("Measured distance = %.1f cm" % dist)
                time.sleep(0.1)
                GPIO.output(GPIO_LED, 0)
                query = Parking.update(status = False).where(Parking.id == 1) #sensor 1
                query.execute()

            if dist2 <= 6:
                print ("Measured distance sensor 2 = %.1f cm" % dist2)
                time.sleep(0.1)
                GPIO.output(GPIO_LED2, 1)
                query2 = Parking.update(status = True).where(Parking.id == 2) #sensor 2
                query2.execute()
            else:
                print ("Measured distance sensor 2 = %.1f cm" % dist2)
                time.sleep(0.1)
                GPIO.output(GPIO_LED2, 0)
                query2 = Parking.update(status = False).where(Parking.id == 2) #sensor 2
                query2.execute()
            
            #while True:
            #    dist = distance()
            #    #print ("Measured Distance = %.1f cm" % dist)
            #    print(dist)
            #    time.sleep(0.5)
    
            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
