#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import connection

def testSendFrame():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	adress = ("localhost", 1212)
	buffer = encode_frame(1, 0, "killian", 0, 1, 0, 0, "")
	send_frame(s, adress, buffer)

	
def testConnection():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	adress = ("localhost", 1212)
	connection.connection(s, adress)


testConnection()
