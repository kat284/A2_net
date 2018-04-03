#~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File type:                ECE 4564 Assignment 2 Python Script
# File name:                Led File (led.py)
# Description:              Script containing the setup and running of the led portion of the server
# Inputs/Resources:
# Output/Created files:     Led Responses
# Written by:               Team 6
# Created:                  04/02/2018
# Last modified:            04/02/2018
# Version:                  1.0.0
# Example usage:            python3 led.py -s <RMQ IP OR HOSTNAME>
#                                               -m <GPIO MODE>
#                                               -r <RED PIN NUMBER>
#                                               -g <GREEN PIN NUMBER>
#                                               -b <BLUE PIN NUMBER>
# Notes:                    N/A
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3

import RPi.GPIO as GPIO

#Server Command:

#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

RMQ_IP = "localhost"
GPIO_MODE = 10
RED_PIN = 0
GREEN_PIN = 0
BLUE_PIN = 0

#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def loadOptions(argv):
    global RMQ_IP 
    global GPIO_MODE 
    global RED_PIN 
    global GREEN_PIN 
    global BLUE_PIN 
    
    options = {}
    while argv:
        if argv[0][0] == '-':
            options[argv[0]] = argv[1]
        argv = argv[1:]
    if (len(options) == 5) and ('-s' in options) and ('-m' in options) and ((options['-m'] == 10) or (options['-m'] == 11))  and ('-r' in options) and ('-g' in options) and ('-b' in options):
        RMQ_IP = options['-s']
        GPIO_MODE = options['-m']
        RED_PIN = options['-r']
        GREEN_PIN = options['-g']
        BLUE_PIN = options['-b']
    else:
        return 1
    return 0

def callback(ch,method,properties,body):
	if body == "red":
		GPIO.output(RED_PIN,GPIO.HIGH)
		GPIO.output(GREEN_PIN,GPIO.LOW)
		GPIO.output(BLUE_PIN,GPIO.LOW)
	elif body == "blue":
		GPIO.output(RED_PIN,GPIO.LOW)
		GPIO.output(GREEN_PIN,GPIO.LOW)
		GPIO.output(BLUE_PIN,GPIO.HIGH)
	elif body == "purple":
		GPIO.output(RED_PIN,GPIO.HIGH)
		GPIO.output(GREEN_PIN,GPIO.LOW)
		GPIO.output(BLUE_PIN,GPIO.HIGH)
	elif body == "yellow":
		GPIO.output(RED_PIN,GPIO.HIGH)
		GPIO.output(GREEN_PIN,GPIO.HIGH)
		GPIO.output(BLUE_PIN,GPIO.LOW)
	elif body == "green":
		GPIO.output(RED_PIN,GPIO.LOW)
		GPIO.output(GREEN_PIN,GPIO.HIGH)
		GPIO.output(BLUE_PIN,GPIO.LOW)
	print("[Checkpoint] Flashing LED to ",body)
 
#~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#       
        
if __name__ == '__main__':

	if loadOptions(sys.argv):
		print('[ERROR] Arguments missing or are incorrect')
 		print('[ERROR] CLOSING')
		sys.exit(1)   
    if GPIO_MODE == 10:
		GPIO.setmode( GPIO.BOARD)
    else:
		GPIO.setmode( GPIO.BCM)  
	GPIO.setup(RED_PIN,GPIO.OUT)
	GPIO.setup(GREEN_PIN,GPIO.OUT)
	GPIO.setup(BLUE_PIN,GPIO.OUT)
	credentials = pika.PlainCredentials(username=rmq_params.get("username"),password=rmq_params.get("password"))
	parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=rmq_params.get("vhost"),credentials=credentials)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	print("[Checkpoint] Connected to vhost ", rmq_params.get("vhost") ," on RMQ server at ", RMQ_IP," as user ",rmq_params.get("username"))
	channel.queue_bind(exchange=rmq_params.get("exchange"),queue=rmq_params.get("led_queue"),rmq_params.get("led_queue"))
	channel.basic_consume(callback,queue=rmq_params.get("led_queue"),no_ack=True)
	print("[Checkpoint] Consuming from RMQ queue: ",rmq_params.get("led_queue"))
	channel.start_consuming()
	print('[ERROR] No longer consuming')
	GPIO.cleanup()
	connection.close()

#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
