#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import connection


def encode_frame(_id, _type, username, zone, state, ack_state, error_state, data):
	""" Return the buffer encoded """
    # concat id and type
	idtype = (_id << 1) + _type
    # concat state, ack_state, error_state
	state_ackSt_ackEr = (state << 6) + (ack_state << 4) + error_state
    # create the buffer
	buf = ctypes.create_string_buffer(15 + len(data))
    # fill the buffer, the data length is variable
	struct.pack_into('H10sHB' + str(len(data)) + 's', buf, 0,  idtype, username, zone, state_ackSt_ackEr, data)
	return buf
	
	
def send_frame(socket, adress, buf):
	""" Send a frame with parameters encoded to the adress """
	# send the buffer
	socket.sendto(buf, adress)


def decode_frame(buf):
	""" Return the value of a frame received """
	data_size = len(buf) - 15
	frame = {}

	idType = struct.unpack('H', buf[0:2])[0]
	frame["id"] = idType >> 1
	frame["type"] = idType % 2

	frame["username"] = struct.unpack("10s", buf[2:12])[0]
	frame["zone"] = struct.unpack("H", buf[12:14])[0]

	state_ackSt_ackEr = struct.unpack("B", buf[14])[0]
	frame["state"] = state_ackSt_ackEr >> 6
	frame["ack_state"] = (state_ackSt_ackEr >> 4) % 4
	frame["error_state"] = state_ackSt_ackEr % 16

	frame["data"] = struct.unpack(str(data_size) + "s", buf[15:(15 + data_size)])[0]
	#logger.info("//ID:"+str(frame["id"])+"//TYPE:"+str(frame["type"])+"//UTILISATEUR:"+str(frame["username"])+"//ZONE:"+str(frame["zone"])+"//STATE:"+str(frame["state"])+"//ACK STATE:"+str(frame["ack_state"])+"//ERREUR STATE:"+str(frame["error_state"])+"//DATA:"+str(frame["data"]))
	return frame
