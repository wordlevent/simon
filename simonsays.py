#########Simon Says#################
####################################
#####Copyright 2013-Alex Stange#####

#This is a game designed for a raspberry pi connected to a circuit using the GPIO pins. 
#The computer will randomly come up with a sequence of Red, Yellow, or Green lights which the user must correctly repeat.
#After each successful completion the sequence grows by 1 in length




from time import sleep, clock, time
import RPi.GPIO as GPIO
import random
import os

GPIO.setmode(GPIO.BOARD)

def start():			#will run when the program starts
		light("R")
		sleep(.05)
		light("Y")
		sleep(.05)
		light("G")
		sleep(.05)
		allOff()
		sleep(.05)


def lost():				#will run when the user loses
		light("G")
		sleep(.05)
		light("Y")
		sleep(.05)
		light("R")
		sleep(.05)
		allOff()
		sleep(.05)


def light(color):		#function which takes a string: R, Y or G and fires the corresponding GPIO pin and sound file
	GPIO.setup(12, GPIO.OUT) #red
	GPIO.setup(16, GPIO.OUT) #yellow
	GPIO.setup(18, GPIO.OUT) #green
	if color == "R":
		GPIO.output(12, GPIO.HIGH)
		os.system('aplay 440.wav')
	if color == "Y":
		GPIO.output(16, GPIO.HIGH)
		os.system('aplay 660.wav')
	if color == "G":
		GPIO.output(18, GPIO.HIGH)
		os.system('aplay 880.wav')

		
def allOff():			#turns all GPIO pins to low
	GPIO.setup(12, GPIO.OUT) #red
	GPIO.setup(16, GPIO.OUT) #yellow
	GPIO.setup(18, GPIO.OUT) #green
	GPIO.output(12, GPIO.LOW)
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)		


def chosen():			#this function will switch the GPIOs to input mode and return which button is pressed
	
	condition=True
	
	GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #red
	GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #yellow
	GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #green
	
	while (condition):
		
		red_prev_input_value=False
		red_input_value=GPIO.input(12)
		
		yellow_prev_input_value=False
		yellow_input_value=GPIO.input(16)
			
		green_prev_input_value=False
		green_input_value=GPIO.input(18)
		
		if ((not red_prev_input_value) and red_input_value):
			os.system('aplay 440.wav')
			return "R"
			red_prev_input_value=red_input_value
			sleep(0.1)
			condition=False
			
		if ((not yellow_prev_input_value) and yellow_input_value):
			os.system('aplay 660.wav')
			return "Y"
			yellow_prev_input_value=yellow_input_value
			sleep(0.1)
			condition=False
		
		if ((not green_prev_input_value) and green_input_value):
			os.system('aplay 880.wav')
			return "G"
			green_prev_input_value=green_input_value
			sleep(0.1)
			condition=False
			


def showScore(r):			#this function tells the user their score by lighting R for ones, Y for tens, and G for hundreds
	ones = r%10
	tens = (r%100 - r%10)/10
	hundreds = (r - r%100)/100
	
	for x in range(0, hundreds):
		light("G")
		sleep(.1)
		allOff()
		sleep(.1)
		
	for x in range(0, tens):
		light("Y")
		sleep(.1)
		allOff()
		sleep(.1)
	
	for x in range(0, ones):
		light("R")
		sleep(.1)
		allOff()
		sleep(.1)

########THE GAME#############

playing = True
round = 0
sequence = [None]*100
start()

while playing: #this loop is one round of play
	sequence[round] = random.choice(["R","Y","G"])
		
	for x in range(0, (round+1)):
		light(sequence[x])
		#BEEP?
		sleep(.3)
		allOff()
		sleep(.3)
		
	for x in range(0,100):				#the sequence is printed to a command line...don't look at your monitor if you want to play for real!
		if (sequence[x] != None):
			print(sequence[x])
				
	sleep(.2);
	
	i = 0;
	while (i < (round+1)):   #this loop checks user's input sequence and will continue of correct or end if incorrect

		userChoice = chosen()
		print("user: "+userChoice)
		
		if ((userChoice != sequence[i]) and (userChoice != None)):
			print("WRONG")
			playing = False
			i=round+1
		else:
			print("Correct")
			sleep(.4)
			i += 1

			
	sleep(1);
	round += 1;
	
sleep(.5)
lost()
showScore(round)

allOff();
GPIO.cleanup()
