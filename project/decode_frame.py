#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket


def decode_frame(buf):
	""" Return the value of a frame received """
	data_size = len(buf) - 15
	frame = {}

	idType = struct.unpack('H', buf[0:2])[0]
	print idType
	frame["id"] = idType >> 1
	frame["type"] = idType % 2

	frame["username"] = struct.unpack("10s", buf[2:12])[0]
	frame["zone"] = struct.unpack("H", buf[12:14])[0]

	state_ackSt_ackEr = struct.unpack("B", buf[14])[0]
	frame["state"] = state_ackSt_ackEr >> 6
	frame["ack_state"] = (state_ackSt_ackEr >> 4) % 4
	frame["error_state"] = state_ackSt_ackEr % 16

	frame["data"] = struct.unpack(str(data_size) + "s", buf[15:(15 + data_size)])[0]
	return frame
