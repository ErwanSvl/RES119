#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import frame_manager
import connection
import settings

POWER_ON = True

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((settings.HOST, settings.PORT))

while POWER_ON:
    buf, adress = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    frame_manager.print_frame(frame)
    if frame["type"] == 0:  # Data frame
        if frame["zone"] == 0:  # Public canal
            if frame["state"] == 0:  # Default (Message)
                frame_manager.send_frame_public(s, adress, buf)
            elif frame["state"] == 1:  # Connection
                connection.connectionAnswer(s, adress, frame["username"], frame["id"] + 1)
            elif frame["state"] == 2:  # Deconnection
                print "Empty"
            elif frame["state"] == 3:  # Server command
                print "Empty"
            else:  # Bad entry
                print "Empty"
        elif frame["zone"] == 1:  # Centralized private canal
            print "Empty"
        elif frame["zone"] == 2:  # Decentralized private canal
            print "Empty"
        else:  # Bad entry zone parameter
            print "Empty"
    else:  # Ack frame
        print 'Empty'
