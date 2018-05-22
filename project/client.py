#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import os
import connection
import frame_manager
import settings

def testSendFrame(s, adress):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	adress = ("localhost", 1212)
	buf = frame_manager.encode_frame(1, 0, "killian", 0, 1, 0, 0, "")
	frame_manager.send_frame_to_server(s, adress, buf)

	
def testConnection(s, adress):
	print "Connexion Request"
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	adress = ("localhost", 1212)
	connection.connectionRequest(s, adress)
	buf, adress = s.recvfrom(settings.FRAME_LENGTH)
	frame = frame_manager.decode_frame(buf)
	frame_manager.print_frame(frame)

CONNECTED = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
adress = (settings.HOST, settings.PORT)

while not CONNECTED :
	connection.connectionRequest(s, adress)
	buf, adresse = s.recvfrom(settings.FRAME_LENGTH)
	frame = frame_manager.decode_frame(buf)
	if frame["ack_state"] == 1 :
		CONNECTED = True
	elif frame["error_state"] == 1 :
		print "Echec de la connexion : votre login est déjà utilisé."
	elif frame["error_state"] == 2 :
		print "Echec de la connexion : trop de clients connectés."
print "Connected\n"

POWER_ON = True
childPID = os.fork()

while(POWER_ON) :
	if childPID == 0 :
		buf, adresse = s.recvfrom(settings.FRAME_LENGTH)
		frame = frame_manager.decode_frame(buf)
		frame_manager.print_frame(frame)

	else :
		msg = raw_input()
		
		if msg == "!q":
			s.sendto("disconnected_client", adress)
			os.kill(childPID, 9)
			POWER_ON = False
		else:
			s.sendto(msg, adress)

print "Disconnected"

