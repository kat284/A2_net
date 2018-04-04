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
ORDER_ID = 0
    
#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    try:
        connection = 0
        credentials = pika.PlainCredentials(username=rmq_params.get("username"),password=rmq_params.get("password"))
        parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=rmq_params.get("vhost"),credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except:
        print("[ERROR] Unable to connect to vhost: ",rmq_params.get("vhost")," on RMQ server at ", RMQ_IP," as user ",rmq_params.get("username"))
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct!")
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        exit(1)
    print("[Checkpoint] Connected to vhost ", rmq_params.get("vhost") ," on RMQ server at ", RMQ_IP," as user ",rmq_params.get("username"))
    print("[Checkpoint] Setting up exchanges and queues...")
    channel.exchange_declare(rmq_params.get("exchange"), exchange_type='direct')
    channel.queue_declare(rmq_params.get("order_queue"), auto_delete=True)
    channel.queue_declare(rmq_params.get("led_queue"), auto_delete=True)
    channel.queue_bind(exchange=rmq_params.get("exchange"),queue=rmq_params.get("order_queue"),routing_key=rmq_params.get("order_queue"))
    channel.queue_bind(exchange=rmq_params.get("exchange"),queue=rmq_params.get("led_queue"),routing_key=rmq_params.get("led_queue"))
    try:
        server_socket = 0
        server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        server_socket.bind((RMQ_IP,RFCOMM_CHANNEL))
        server_socket.listen(1)
    except:
        print("[ERROR] Unable to open the socket")
        print("[ERROR] Bluetooth socket CLOSING")
        if server_socket:
            server_socket.close()
        connection.close()
        exit(1)
    print("[Checkpoint] Bluetooth ready!")
    print("[Checkpoint] Waiting for connection on RFCOMM channel ", RFCOMM_CHANNEL)
    while 1:
        try:
            client_socket = 0
            client_socket, address = server_socket.accept()
            print("[Checkpoint] Accepted connection from ",address)
            channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=rmq_params.get("led_queue"),body="blue")
            client_socket.send(str(menu))
            print("[Checkpoint] Sent menu: ",menu)
            #Clearer menu output
            order = eval(str(client_socket.recv(1024),'utf-8'))
            print("[Checkpoint] Received order: ",order)
            ORDER_ID = ORDER_ID + 1
            total_price = 0
            total_time = 0
            for item in order:
                info = menu.get(item)
                total_price = total_price + info.get("price")
                total_time = total_time + info.get("time")
            receipt = {"Order ID": ORDER_ID, "Items": order, "Total Price": total_price, "Total Time" :total_time}
            str_receipt = str(receipt)
            client_socket.send(str_receipt)
            print("[Checkpoint] Sent receipt: ",str_receipt)
            #Clearer receipt output
            channel.queue_declare(str(ORDER_ID), auto_delete=True)
            channel.queue_bind(exchange=rmq_params.get("exchange"),queue=str(ORDER_ID),routing_key=str(ORDER_ID))
            channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=rmq_params.get("order_queue"),body=str_receipt)
            submit_msg = "Order Update: Your order has been submitted"
            channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=str(ORDER_ID),body=submit_msg)
            client_socket.close()
            channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=rmq_params.get("led_queue"),body="red")
            print("[Checkpoint] Closed Bluetooth Conection")
        except:
            print("[ERROR] Communication with the Client Lost or the server.py process was killed")
            print("[ERROR] Bluetooth socket CLOSING")
            if client_socket:
                client_socket.close()
            server_socket.close()
            connection.close()
            exit(1)
  
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
