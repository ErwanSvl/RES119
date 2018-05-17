#-*- coding:utf-8 -*-

import ctypes
import struct
import argparse
import socket

def send_frame(socket, adress, buf):
	""" Send a frame with parameters encoded to the adress """
	# send the buffer
	socket.sendto(buf, adress)
