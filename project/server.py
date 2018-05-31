# -*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import socerr
import frame_manager
import connection
import settings

POWER_ON = True
current_id = 0

s = socerr.socerr(socket.AF_INET, socket.SOCK_DGRAM, settings.ERROR_RATE)
s.bind((settings.HOST, settings.PORT))

while POWER_ON:
    buf, adress = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    frame_manager.print_frame(frame)
    if frame["type"] == 0:  # Data frame
        if frame["zone"] == 0:  # Public canal
            if frame["state"] == 0:  # Default (Message)
                for client in settings.CLIENTS_CONNECTED:
                    if client["adress"] == adress:  # Find the sender
                        frame_manager.send_ack(adress, s, frame)
                        # if the ID is the same : this message is a reemission
                        if client["id"] != frame["id"]:
                            client["id"] = frame["id"]
                            current_id = frame_manager.send_frame_public(
                                s, adress, buf, current_id)
            elif frame["state"] == 1:  # Connection
                connection.connectionAnswer(
                    s, adress, frame["username"], frame["id"])
            elif frame["state"] == 2:  # Deconnection
                current_id = connection.deconnectionAnswer(
                    s, adress, frame["username"], frame["id"], current_id)
            elif frame["state"] == 3:  # Server command
                print "Not implemented yet"
            else:  # Bad entry
                print "Bad Entry"
        elif frame["zone"] == 1:  # Centralized private canal
            print "Not implemented yet"
        elif frame["zone"] == 2:  # Decentralized private canal
            print "Not implemented yet"
        else:  # Bad entry zone parameter
            print "Bad Entry"
    else:  # Ack frame
        frame_manager.defuseTimer(socket, adress)
