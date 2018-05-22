#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import frame_manager

HOST = "localhost"
PORT = 1212
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
message, adress = s.recvfrom(1415)
print "message recu! :"
frame = frame_manager.decode_frame(message)
print "		ID : "+str(frame["id"])
print "		TYPE : "+str(frame["type"])
print "		UTILISATEUR : "+str(frame["username"])
print "		ZONE : "+str(frame["zone"])
print "		STATE : "+str(frame["state"])
print "		ACK STATE : "+str(frame["ack_state"])
print "		ERREUR STATE : "+str(frame["error_state"])
print "		DATA : "+str(frame["data"])
