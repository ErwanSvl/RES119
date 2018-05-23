#-*- coding:utf-8 -*-
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
    connection.connectionRequest(s, adress, ID)
    buf, adress = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    frame_manager.print_frame(frame)


ID = random.randint(1, 32767)
CONNECTED = False

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
adress = (settings.HOST, settings.PORT)

while not CONNECTED:
    username = connection.connectionRequest(s, adress, ID)
    buf, adresse = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    ID = frame_manager.incremente_id(ID)
    frame_manager.print_frame(frame)
    if frame["ack_state"] == 1:
        CONNECTED = True
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
            ID = frame_manager.incremente_id(ID)
            buf = frame_manager.encode_frame(ID, 0, username, 0, 0, 0, 0, msg)
            frame_manager.send_frame(s, adress, buf)
        else:  # The user receiving a message
            buf, adresse = s.recvfrom(settings.FRAME_LENGTH)
            frame = frame_manager.decode_frame(buf)
            # Incremente the ID if this is a data frame
            ID = frame_manager.incremente_id(ID)
            frame_manager.print_frame(frame)
            print str(frame["username"])+" : "+frame["data"]
