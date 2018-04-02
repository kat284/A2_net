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

RMQ_IP = "localhost"
RFCOMM_CHANNEL = 3

#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':

	order_id = 0
	
	credentials = pika.PlainCredentials(username=rmq_params.get("username"),password=rmq_params.get("password"))
	parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=rmq_params.get("vhost"),credentials=credentials)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	print("[Checkpoint] Connected to vhost ", rmq_params.get("vhost") ," on RMQ server at ", RMQ_IP," as user ",rmq_params.get("username"))
	print("[Checkpoint] Setting up exchanges and queues...")
	channel.exchange_declare(rmq_params.get("exchange"), exchange_type='direct')
	channel.queue_declare(rmq_params.get("order_queue"), auto_delete=True)
	channel.queue_declare(rmq_params.get("led_queue"), auto_delete=True)
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	server_sock.bind((RMQ_IP,RFCOMM_CHANNEL))
	server_sock.listen(1)
	bluetooth.advertise_service(server_sock, "Assignment_2_Service",
                     service_classes=[bluetooth.SERIAL_PORT_CLASS],
                     profiles=[bluetooth.SERIAL_PORT_PROFILE])
	print("[Checkpoint] Bluetooth ready!")
	print("[Checkpoint] Waiting for connection on RFCOMM channel ", RFCOMM_CHANNEL)
	while 1:
		client_sock, address = server_sock.accept()
		print("[Checkpoint] Accepted connection from ",address)
		channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=rmq_params.get("led_queue"),body="blue")
		client_socket.sent(menu)
		print("[Checkpoint] Sent menu: ",menu)
		order = client_sock.recv(1024)
		print("[Checkpoint] Received order: ",items)
		order_id = order_id + 1
		total_price = 0
		total_price = 0
		for item in items:
			info = menu.get(item)
			total_price = total_price + info.get("price")
			total_time = total_time + minfo.get("time")
		receipt = "Order ID: " + str(order_id) + "\nItems: " + str(items) + "\nTotal Price: " + str(total_price) + "\nTotal Time: " + str(total_time)
		client_socket.sent(receipt)
		channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=rmq_params.get("order_queue"),body=receipt)
		print("[Checkpoint] Sent receipt: ",receipt)
		channel.queue_declare(str(order_id), auto_delete=True)
		submit_msg = "Order Update: Your order has been submitted"
		channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=str(order_id),body=submit_msg)
		client_sock.close()
		channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=rmq_params.get("led_queue"),body="red")
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

    except socket.error as error_message:
        print("[ERROR] Unable to open the socket: " + str(error_message))
        print('[ERROR] Server CLOSING')
        sys.exit(1)
 """   
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
