#~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File type:                ECE 4564 Assignment 2 Python Script
# File name:                Server File (server.py)
# Description:              Script containing the setup and running of the server
# Inputs/Resources:
# Output/Created files:     Server Side Responses
# Written by:               Team 6
# Created:                  04/02/2018
# Last modified:            04/02/2018
# Version:                  1.0.0
# Example usage:            python3 server.py
# Notes:                    N/A
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3
"""
import socket
import sys
import pickle
import os
from cryptography.fernet import Fernet
import hashlib
"""
from rmq_params import *
from menu import *
import bluetooth
from bluetooth import *
import pika
#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

RMQ_IP = '0.0.0.0'
RFCOMM_CHANNEL = 1
SOCKET_SIZE = 1024
BACKLOG_SIZE= 5
SERVER = None

#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def loadOptions(argv):
    global SERVER_PORT
    global SOCKET_SIZE
    global BACKLOG_SIZE


if __name__ == '__main__':

	order_id = 0
	
	credentials = pika.Plaincredentials(rmq_params.get("username"),rmq_params.get("password"))
	parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=rmq_params.get("vhost"),credentials=credentials)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	print("[Checkpoint] Connected to vhost ", rmq_params.get("vhost") ," on RMQ server at ", RMQ_IP," as user ",rmq_params.get("username"))
	print("[Checkpoint] Setting up exchanges and queues...")
	channel.exchange_declare(rmq_params.get("exchange"), exchange_type='direct')
	channel.queue_declare(rmq_params.get("order_queue"), auto_delete=True)
	channel.queue_declare(rmq_params.get("led_queue"), auto_delete=True)
	#channel.queue_bind(exchange=rmq_params.get("exchange"),queue=rmq_params.get("order_queue"),routing_key="")
	#channel.queue_bind(exchange=rmq_params.get("exchange"),queue=rmq_params.get("led_queue"),routing_key="")	
	
	
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	server_sock.bind(("",RFCOMM_CHANNEL))
	server_sock.listen(1)
	bluetooth.advertise_service(server_sock, "SampleServer",
                     service_classes=[bluetooth.SERIAL_PORT_CLASS],
                     profiles=[bluetooth.SERIAL_PORT_PROFILE])
	print("[Checkpoint] Bluetooth ready!")
	print("[Checkpoint] Waiting for connection on RFCOMM channel ",RFCOMM_CHANNEL)
	while(1)
		client_sock, address = server_sock.accept()
		print("[Checkpoint] Accepted connection from ",address)
			channel.basic_publish(exchange='',routing_key='hello',body='Hello World!')
		#SEND UPDATE TO LED QUEUE
		client_socket.sent(menu)
		print("[Checkpoint] Sent menu: ",menu)
		order = client_sock.recv(1024)
		print("[Checkpoint] Received order: ",items)
		order_id = order_id + 1
		total_price = 0
		total_price = 0
		for item in items
			info = menu.get(item)
			total_price = total_price + info.get("price")
			total_time = total_time + minfo.get("time")
		receipt = "Order ID: " + str(order_id) + "\nItems: " + str(items) 
								+ "\nTotal Price: " + str(total_price) 
								+ "\nTotal Time: " + str(total_time)
		client_socket.sent(receipt)
		#SEND TO PROCESSOR QUEUE
		print("[Checkpoint] Sent receipt: ",receipt)
		#CREATE ANOTHER QUEUE NAME IS ORDER ID
		submit_msg = "Order Update: Your order has been submitted"
		#SEND SUBMIT MESSAGE TO NEW QUEUE
		client_sock.close()
		#SEND UPDATE TO LED QUEUE
		print("[Checkpoint] Closed Bluetooth Conection")
	server_sock.close()
	connection.close()

"""
    if loadOptions(sys.argv):
        print('[ERROR] Arguments missing or are incorrect')
        print('[ERROR] Server CLOSING')
        sys.exit(1)
    wfa_client = wolframalpha.Client(wolfram_alpha_appid)
    try:
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        SERVER.bind((SERVER_IP,int(SERVER_PORT)))
        print('[Checkpoint] Created socket at ', SERVER_IP, ' on port ', SERVER_PORT)
        SERVER.listen(int(BACKLOG_SIZE))
    except socket.error as error_message:
        if SERVER :
            SERVER.close()
        print("[ERROR] Unable to open the socket: " + str(error_message))
        print('[ERROR] Server CLOSING')
        sys.exit(1)
    while 1:
        print('[Checkpoint] Listening for client connections')
        client, address = SERVER.accept()
        print('[Checkpoint] Accepted client connection from ', SERVER_IP, ' on port ', SERVER_PORT)
        data = client.recv(int(SOCKET_SIZE))
        print('[Checkpoint] Received data: ', data)
        if data:
            message_receive = pickle.loads(data)
            if hashlib.md5(message_receive[1]).hexdigest() != message_receive[2]:
                print('[ERROR] Checksum is NOT VALID')
                print('[ERROR] Server CLOSING')
                sys.exit(1)
            else:
                print('[Checkpoint] Checksum is VALID')
                text_msg = Fernet(message_receive[0]).decrypt(message_receive[1])
                print('[Checkpoint] Decrypt: Using Key: ', message_receive[0], ' | Plaintext: ', text_msg)
                text_msg = text_msg.decode("utf-8")
                cmd = 'espeak "{0}" 2>/dev/null'.format(text_msg)
                os.system(cmd)
                print('[Checkpoint] Speaking: ', text_msg)
                print('[Checkpoint] Sending question to Wolframalpha: ', text_msg)
                res = wfa_client.query(text_msg)
                answer = next(res.results).text
                text_msg = str(answer)
                print('[Checkpoint] Received question from Wolframalpha: ', text_msg)
                en_msg = Fernet(message_receive[0]).encrypt(text_msg.encode('utf-8'))
                print('[Checkpoint] Encrypt: Generated Key: ', message_receive[0], ' | Ciphertext: ', en_msg)
                check_msg = hashlib.md5(en_msg).hexdigest()
                print('[Checkpoint] Generated MD5 Checksum: ', check_msg)
                message_send = (en_msg, check_msg)
                pickle_msg = pickle.dumps(message_send)
                print('[Checkpoint] Sending data: ', pickle_msg)
                client.send(pickle_msg)
        else:
            print('[ERROR] Unknown packet received')
        client.close()
"""
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
