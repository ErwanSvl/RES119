#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import encode_frame
import send_frame

def connection(socket, adress):
	""" Client connect to the server """
	print "Entrez votre nom d'utilisateur :"
	username = raw_input()
	
	#Verify that username is shorter than or equal to 10 characters and longer than 0
	while(len(username) > 10) or (len(username) < 1):
		print username
		print len(username)
		print "Le nombre de charactères doit être compris entre 1 et 10 :"
		username = raw_input()
		for i in range(10-len(username)):
			username += " "
	
	#Encode the frame before sending
	buf = encode_frame.encode_frame(1, 0, username, 0, 1, 0, 0, "")
	#Send the encoding frame
	send_frame.send_frame(socket, adress, buf)
