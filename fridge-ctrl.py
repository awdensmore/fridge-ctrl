
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import time

for sensor in W1ThermSensor.get_available_sensors():
    print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)
#GPIO.output(26, GPIO.HIGH)

# Set points
t_h = 16 # turn fridge on above this
t_l = 15 # turn fridge off below this
dly = 1*60 # Switch delay

# Startup
status = 0
time_old = time.time()
print("Time is: " + str(time_old))
if sensor.get_temperature() > t_h:
	GPIO.output(26,GPIO.HIGH)
	status = 1

while(1):
	now = time.time()
	
	if (time.time() - time_old) > dly:
		temp = sensor.get_temperature()

		if temp > t_h:
			GPIO.output(26, GPIO.HIGH)
			status = 1
		elif temp < t_l:
			GPIO.output(26, GPIO.LOW)
			status = 0

		#print(str(now) + " Temp: " + str(temp) + "\n")
		f = open('fridge-log.txt', 'a')
		f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			+ " Temp: " + str(temp) + " Fridge status: " + str(status) + "\n")
		f.close()
		time_old = now

GPIO.cleanup()
