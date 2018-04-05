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
# Last modified:            04/03/2018
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
import bluetooth
import sys
import pika
from rmq_params import *

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
    if (len(options) == 5) and ('-s' in options) and ('-m' in options) and ((options['-m'] == "10") or (options['-m'] == "11"))  and ('-r' in options) and ('-g' in options) and ('-b' in options):
        RMQ_IP = options['-s']
        GPIO_MODE = eval(options['-m'])
        RED_PIN = eval(options['-r'])
        GREEN_PIN = eval(options['-g'])
        BLUE_PIN = eval(options['-b'])
    else:
        return 1
    return 0

def callback(ch,method,properties,body):
   body=str(body,'utf-8')
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
   print("[Checkpoint] Flashing LED to {0}".format(body))
   
 
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
   if GPIO_MODE == "10":
      GPIO.setmode( GPIO.BOARD)
   else:
      GPIO.setmode( GPIO.BCM)  
   GPIO.setup(RED_PIN,GPIO.OUT) 
   GPIO.setup(GREEN_PIN,GPIO.OUT) 
   GPIO.setup(BLUE_PIN,GPIO.OUT) 
   try:
        connection = 0
        credentials = pika.PlainCredentials(username=rmq_params.get("username"),password=rmq_params.get("password"))
        parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=rmq_params.get("vhost"),credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
   except:
        print("[ERROR] Unable to connect to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(rmq_params.get("vhost"),RMQ_IP, rmq_params.get("username")))
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct!")
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        GPIO.cleanup() 
        exit(1)
   print("[Checkpoint] Connected to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(rmq_params.get("vhost"),RMQ_IP, rmq_params.get("username")))
   try:
       channel.queue_bind(exchange=rmq_params.get("exchange"),queue=rmq_params.get("led_queue"),routing_key=rmq_params.get("led_queue")) 
       channel.basic_consume(callback,queue=rmq_params.get("led_queue"),no_ack=True) 
       print("[Checkpoint] Consuming from RMQ queue: {0}".format(rmq_params.get("led_queue"))) 
       channel.start_consuming() 
   except:
       print("[ERROR] The queue ({0}) was not found or the led.py process was killed".format(rmq_params.get("led_queue")))
       print("[ERROR] Verify that the queue is up! You may have to restart the server")
       print("[ERROR] Connection closing")
       connection.close()
       GPIO.cleanup() 
       exit(1)    

#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
