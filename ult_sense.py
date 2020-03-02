import RPi.GPIO as gpio
import time

class ult_sensor:
	
	
	def __init__(self):
		gpio.setmode(gpio.BCM)
		gpio.setwarnings(False)
		#setup GPIO pins for trigger and echo
		self.trigger = 5
		self.echo = 6

		self.trigger2 = 23
		self.echo2 = 17
		self.dist = 0.5
		self.dist2 = 1
		gpio.setup(self.trigger, gpio.OUT)
		gpio.setup(self.echo, gpio.IN)

		gpio.setup(self.trigger2, gpio.OUT)
		gpio.setup(self.echo2, gpio.IN)

		gpio.output(self.trigger, False)
		gpio.output(self.trigger2, False)
		print("Ultrasonic Sensor Ready!")


	def getVert(self):
		try:
			#print "Ultrasonic Measuring"
			#gpio.setup(trigger, gpio.OUT)
			#gpio.setup(echo, gpio.IN)

			#Setup trigger low and then stabilize it
			gpio.output(self.trigger, False)
			time.sleep(0.05) #2

			#start HIGH
			gpio.output(self.trigger, True)

			#provide 10uS pulse to start the ranging
			time.sleep(0.00001)
			gpio.output(self.trigger, False)

			#measure time start
			pulse_send = time.time()
			
			while gpio.input(self.echo) == 0:
				pulse_start = time.time()
				if pulse_start - pulse_send > 0.25:
					print("Missed Ultrasonic")
					return self.dist
					

			#measure time end
			while gpio.input(self.echo) == 1:
				pulse_end = time.time()
					
			#calculate the pulse time
			pulse = pulse_end	-pulse_start

			#time it takes to travel to the object
			dist = pulse * 17150

			#convert distance into m
			dist = dist/100

			#distance to 2 decimals
			self.dist = round(dist,2)
			return self.dist
			
		except Exception as e:
			print(e)
			return None


	def getHorz(self):
		try:
			# Run measurement on horizontal sensor
			#Setup trigger low and then stabilize it
			gpio.output(self.trigger2, False)
			time.sleep(0.05) #2

			#start HIGH
			gpio.output(self.trigger2, True)

			#provide 10uS pulse to start the ranging
			time.sleep(0.00001)
			gpio.output(self.trigger2, False)

			#measure time start
			pulse_send = time.time()
			
			while gpio.input(self.echo2) == 0:
				pulse_start = time.time()
				if pulse_start - pulse_send > 0.25:
					print("Missed Ultrasonic")
					return self.dist2

			#measure time end
			while gpio.input(self.echo2) == 1:
				pulse_end = time.time()
					
			#calculate the pulse time
			pulse = pulse_end	-pulse_start

			#time it takes to travel to the object
			dist2 = pulse * 17150

			#convert distance into m
			dist2 = dist2/100

			#distance to 2 decimals
			self.dist2 = round(dist2,2)
			
			return self.dist2
			
		except Exception as e:
			print(e)
			return None

		
	def close(self):
		gpio.cleanup()
