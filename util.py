#Libraries
import RPi.GPIO as GPIO
import time
from models.parking import Parking

#disable warnings
GPIO.setwarnings(False)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 

#######################
#GPIO_TRIGGER = 17
#GPIO_ECHO = 18
#GPIO_LED = 4

#GPIO_TRIGGER2 = 6
#GPIO_ECHO2 = 12
#GPIO_LED2 = 5

#GPIO_TRIGGER3 = 16
#GPIO_ECHO3 = 13
#GPIO_LED3 = 26
######################
#set GPIO Pins
GPIO_TRIGGER = [17,6,16]
GPIO_ECHO = [18,12,13]
GPIO_LED = [4,5,26]

######################
#GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
#GPIO.setup(GPIO_ECHO, GPIO.IN)
#GPIO.setup(GPIO_LED, GPIO.OUT)

#GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
#GPIO.setup(GPIO_ECHO2, GPIO.IN)
#GPIO.setup(GPIO_LED2, GPIO.OUT)

#GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
#GPIO.setup(GPIO_ECHO3, GPIO.IN)
#GPIO.setup(GPIO_LED3, GPIO.OUT)
######################

#set GPIO direction (IN / OUT)
for i in range(3):
    GPIO.setup(GPIO_TRIGGER[i], GPIO.OUT)
    GPIO.setup(GPIO_ECHO[i], GPIO.IN)
    GPIO.setup(GPIO_LED[i], GPIO.OUT)

def ping(TRIGGER,ECHO):
    ################################
    #GPIO.output(GPIO_TRIGGER, True)
    #GPIO.output(GPIO_TRIGGER2, True)
    #GPIO.output(GPIO_TRIGGER3, True)
    # set Trigger after 0.01ms to LOW
    #time.sleep(0.00001)
    #GPIO.output(GPIO_TRIGGER, False)
    #GPIO.output(GPIO_TRIGGER2, False)
    #GPIO.output(GPIO_TRIGGER3, False)
    ################################
    # send 10us pulse to trigger
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)

    ############################
    #StartTime = time.time()
    #StopTime = time.time()

    #StartTime2 = time.time()
    #StopTime2 = time.time()
    
    #StartTime3 = time.time()
    #StopTime3 = time.time()
    ############################
    # set start/stop for each sensor
    StartTime = time.time()
    
    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    #######################################
    #TimeElapsed = StopTime - StartTime
    #TimeElapsed2 = StopTime2 - StartTime2
    #TimeElapsed3 = StopTime3 - StartTime3
    #######################################
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime

    #################################################
    #distance = round((TimeElapsed * 34300) / 2, 1)
    #distance2 = round((TimeElapsed2 * 34300) / 2, 1)
    #distance3 = round((TimeElapsed3 * 34300) / 2, 1)
    #################################################
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = round((TimeElapsed * 34300) / 2, 1)
    
    return distance
 
def run():
    # if __name__ == '__main__':
    try:
        while True:
            #[dist, dist2, dist3] = distance()
            for i in range(3):
                distance = ping(GPIO_TRIGGER[i], GPIO_ECHO[i])
                #print("sensor", i+1, ": ",distance,"cm")
                if distance <= 7:
                    GPIO.output(GPIO_LED[i], 1)
                    query = Parking.update(status = True).where(Parking.id == i+1) #sensor 1
                    query.execute()
                else:
                    GPIO.output(GPIO_LED[i], 0)
                    query = Parking.update(status = False).where(Parking.id == i+1) #sensor 1
                    query.execute()
                    
            #print("wait")
            time.sleep(0.1)
            
            #if dist <= 6:
            #    print ("Measured distance = %.1f cm" % dist)
            #    time.sleep(0.1)
            #    GPIO.output(GPIO_LED, 1)
            #    query = Parking.update(status = True).where(Parking.id == 1) #sensor 1
            #    query.execute()
            #else:
            #    print ("Measured distance = %.1f cm" % dist)
            #    time.sleep(0.1)
            #    GPIO.output(GPIO_LED, 0)
            #    query = Parking.update(status = False).where(Parking.id == 1) #sensor 1
            #    query.execute()

            #if dist2 <= 6:
            #    print ("     Measured distance sensor 2 = %.1f cm" % dist2)
            #    time.sleep(0.1)
            #    GPIO.output(GPIO_LED2, 1)
            #    query2 = Parking.update(status = True).where(Parking.id == 2) #sensor 2
            #    query2.execute()
            #else:
            #    print ("     Measured distance sensor 2 = %.1f cm" % dist2)
            #    time.sleep(0.1)
            #    GPIO.output(GPIO_LED2, 0)
            #    query2 = Parking.update(status = False).where(Parking.id == 2) #sensor 2
            #    query2.execute()
                
            #if dist3 <= 6:
            #    print("          Measured distance sensor 3 = %.1f cm" % dist3)
            #    time.sleep (0.1)
            #    GPIO.output(GPIO_LED3, 1)
            #    query3 = Parking.update(status = True).where(Parking.id == 3) #sensor 3
            #    query3.execute()
            #else:
            #    print("          Measured distance sensor 3 = %.1f cm" % dist3)#sensor 3
            #    time.sleep (0.1)
            #    GPIO.output(GPIO_LED3, 0)
            #    query3 = Parking.update(status = False).where(Parking.id == 3)
            #    query3.execute()
            
            #while True:
            #    dist = distance()
            #    #print ("Measured Distance = %.1f cm" % dist)
            #    print(dist)
            #    time.sleep(0.5)
    
            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
