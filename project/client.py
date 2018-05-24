# -*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import connection
import frame_manager
import settings
import random
import sys
import select


def testSendFrame(s, adress):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    adress = ("localhost", 1212)
    buf = frame_manager.encode_frame(1, 0, "killian", 0, 1, 0, 0, "")
    frame_manager.send_frame(s, adress, buf)


def testConnection(s, adress):
    print "Connexion Request"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    adress = ("localhost", 1212)
    connection.connectionRequest(s, adress, current_id)
    buf, adress = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    frame_manager.print_frame(frame)


current_id = random.randint(1, 32767)
connected = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
adress = (settings.HOST, settings.PORT)

while not connected:
    username = connection.connectionRequest(s, adress, current_id)
    buf, adresse = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    frame_manager.print_frame(frame)
    if frame["ack_state"] == 1:
        connected = True
    elif frame["error_state"] == 1:
        print "Echec de la connexion : votre login est déjà utilisé."
    elif frame["error_state"] == 2:
        print "Echec de la connexion : trop de clients connectés."
print "Connected\n"

POWER_ON = True

while(POWER_ON):
    rlist, _, _ = select.select([sys.stdin, s], [], [])
    for event in rlist:
        if isinstance(event, file):  # The user is writing a message
            msg = sys.stdin.readline()
            # Incremente the ID before sending
            current_id = frame_manager.incremente_id(current_id)
            if msg[0] == "!":
                if msg[0:len(msg) - 1] == "!quit":
                    buf = frame_manager.encode_frame(
                        current_id, 0, username, 0, 2, 0, 0, "")
                    frame_manager.send_frame(s, adress, buf)
            else:
                buf = frame_manager.encode_frame(
                    current_id, 0, username, 0, 0, 0, 0, msg)
                frame_manager.send_frame(s, adress, buf)
        else:  # The user receiving a message
            # decoding the message
            buf, adresse = s.recvfrom(settings.FRAME_LENGTH)
            frame = frame_manager.decode_frame(buf)

            # detect the message type
            if frame["type"] == 0:  # Data frame
                if frame["zone"] == 0:  # Public canal
                    if frame["state"] == 0:  # Default (Message)
                        frame_manager.print_frame(frame)
                        print frame["username"]+" : "+frame["data"]
                    elif frame["state"] == 2:  # Deconnection
                        s.close()
                        print "Good bye !"
                        sys.exit()
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
