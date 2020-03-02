import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
#gpio.setwarnings(False)
#setup GPIO pins for trigger and echo
trigger = 5
echo = 6

trigger2 = 23
echo2 = 17

gpio.setup(trigger, gpio.OUT)
gpio.setup(echo, gpio.IN)

gpio.setup(trigger2, gpio.OUT)
gpio.setup(echo2, gpio.IN)

gpio.output(trigger, False)
gpio.output(trigger2, False)
time.sleep(0.25) #2

try:
	while(1):

		#print "Ultrasonic Measuring"
		#gpio.setup(trigger, gpio.OUT)
		#gpio.setup(echo, gpio.IN)

		#Setup trigger low and then stabilize it
		gpio.output(trigger, False)
		time.sleep(0.25) #2

		#start HIGH
		gpio.output(trigger, True)

		#provide 10uS pulse to start the ranging
		time.sleep(0.00001)
		gpio.output(trigger, False)

		#measure time start
		while gpio.input(echo) == 0:
			pulse_start = time.time()

		#measure time end
		while gpio.input(echo) == 1:
			pulse_end = time.time()
				
		#calculate the pulse time
		pulse = pulse_end	-pulse_start

		#time it takes to travel to the object
		dist = pulse * 17150

		#convert distance into m
		dist = dist/100

		#distance to 2 decimals
		dist = round(dist,2)
		
		## Run measurement on horizontal sensor
		#Setup trigger low and then stabilize it
		gpio.output(trigger2, False)
		time.sleep(0.2) #2

		#start HIGH
		gpio.output(trigger2, True)

		#provide 10uS pulse to start the ranging
		time.sleep(0.00001)
		gpio.output(trigger2, False)

		#measure time start
		while gpio.input(echo2) == 0:
			pulse_start = time.time()

		#measure time end
		while gpio.input(echo2) == 1:
			pulse_end = time.time()
				
		#calculate the pulse time
		pulse = pulse_end	-pulse_start

		#time it takes to travel to the object
		dist2 = pulse * 17150

		#convert distance into m
		dist2 = dist2/100

		#distance to 2 decimals
		dist2 = round(dist2,2)

		print "-------------\nDistance (Vertical):", dist, "m"
		print "Distance (Horizontal):", dist2, "m"

except Exception as e:
	print(e)
	
finally:
	gpio.cleanup()
	exit(0)


