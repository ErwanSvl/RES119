#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import frame_manager
import settings


def connectionRequest(socket, adress):
	""" Client connect to the server """
	print "Entrez votre nom d'utilisateur :"
	username = raw_input()
	username = username.strip()
	
	#Verify that username is shorter than or equal to 10 characters and longer than 0
	while(len(username) > 10) or (len(username) < 1):
		print username
		print len(username)
		print "Le nombre de charactères doit être compris entre 1 et 10 :"
		username = raw_input()
		for i in range(10-len(username)):
			username += " "
	
	#Encode the frame before sending
	buf = frame_manager.encode_frame(1, 0, username, 0, 1, 0, 0, "")
	#Send the encoding frame
	frame_manager.send_frame(socket, adress, buf)


def connectionAnswer(socket, adress, username):
	
	if len(settings.CLIENTS_CONNECTED) == settings.MAX_CLIENTS : # Number max is reached
		buf = frame_manager.encode_frame(2, 0, "server", 0, 1, 2, 2, "")
		frame_manager.send_frame(socket, adress, buf)
		return
		
	for client in settings.CLIENTS_CONNECTED : # Verify the username is not used
		if username == client[0] :
			buf = frame_manager.encode_frame(2, 0, "server", 0, 1, 2, 1, "")
			frame_manager.send_frame(socket, adress, buf)
			return
	
	settings.CLIENTS_CONNECTED.append([username, adress, 2])
	buf = frame_manager.encode_frame(2, 0, "server", 0, 1, 1, 0, "")
	frame_manager.send_frame(socket, adress, buf)
	
	
