#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket


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
