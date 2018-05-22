#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import connection
import frame_manager

def testSendFrame():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	adress = ("localhost", 1212)
	buffer = frame_manager.encode_frame(1, 0, "killian", 0, 1, 0, 0, "")
	frame_manager.send_frame(s, adress, buffer)

	
def testConnection():
	print "Connexion Request"
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	adress = ("localhost", 1212)
	connection.connectionRequest(s, adress)


testConnection()
