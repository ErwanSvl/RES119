# -*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import frame_manager
import connection
import settings

POWER_ON = True
current_id = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((settings.HOST, settings.PORT))

while POWER_ON:
    buf, adress = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    frame_manager.print_frame(frame)
    if frame["type"] == 0:  # Data frame
        if frame["zone"] == 0:  # Public canal
            if frame["state"] == 0:  # Default (Message)
                for client in settings.CLIENTS_CONNECTED:
                    if client["adress"] == adress:
                        print "client id : "+str(client["id"])
                        print "frame id : "+str(frame["id"])
        #########################################################################
                        if client["id"] == frame["id"]:
                            print "Not implemented yet"
                            # TODO : Send ACK
                            #buf_ack = frame_manager.encode_frame(frame["id"], 1, "", 0, 0, 0, 0, "")
                            # frame_manager.send_frame(s, adress, buf_ack) # Send ack to the client sender
                        else:
                            client["id"] = frame["id"]
                            current_id = frame_manager.send_frame_public(
                                s, adress, buf, current_id)
        #########################################################################

            elif frame["state"] == 1:  # Connection
                connection.connectionAnswer(
                    s, adress, frame["username"], frame["id"])
        #########################################################################
            elif frame["state"] == 2:  # Deconnection
                current_id = connection.deconnectionAnswer(
                    s, adress, frame["username"], frame["id"], current_id)
            elif frame["state"] == 3:  # Server command
                print "Empty"
            else:  # Bad entry
                print "Bad Entry"
        elif frame["zone"] == 1:  # Centralized private canal
            print "Not implemented yet"
        elif frame["zone"] == 2:  # Decentralized private canal
            print "Not implemented yet"
        else:  # Bad entry zone parameter
            print "Bad Entry"
    else:  # Ack frame
        print 'Not implemented yet'
