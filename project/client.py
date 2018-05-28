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
from threading import Thread, Event
from Timer import Timer


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

dic = {}
dic["adress"] = None
dic["stop_flag"] = None
dic["timer"] = None
dic["username"] = "server"
dic["wait_msg"] = []
dic["zone"] = 0
dic["id"] = 0

settings.CLIENTS_CONNECTED.append(dic)
print "Connected\n"

while(settings.POWER_ON):
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
                    print "Error : la commande saisie est invalide, les commandes sont appelées via un '!' en début de message"
            else:
                buf = frame_manager.encode_frame(
                    current_id, 0, username, 0, 0, 0, 0, msg)
                frame_manager.send_frame(s, adress, buf)

                if settings.CLIENTS_CONNECTED[0]["timer"] == None:
                    frame_manager.client_timer_init(adress, s, buf, 0)
                else :
                    settings.CLIENTS_CONNECTED[0]["wait_msg"].append(frame_manager.decode_frame(buf))

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
                frame_manager.print_frame(frame)
                # Detect if Ack frame ID receive is equals to the ID of the frame message that timer is waiting for 
                if frame["id"] == settings.CLIENTS_CONNECTED[0]["timer"].getID(): # Ack ID match with timer's frame ID  
                    settings.CLIENTS_CONNECTED[0]["stop_flag"].set()

                    # Try if "wait_msg" is empty
                    if len(settings.CLIENTS_CONNECTED[0]["wait_msg"]) == 0: # "wait_msg" is empty
                        settings.CLIENTS_CONNECTED[0]["timer"] = None
                    else: # "wait_msg" is not empty
                        settings.CLIENTS_CONNECTED[0]["timer"] = None
                        frame_manager.client_timer_init(adress, socket, buf)

                else: # Ack ID doesn't match with timer's frame ID

                    # Try if "wait_msg" is empty
                    if len(settings.CLIENTS_CONNECTED[0]["wait_msg"]) > 0: # "wait_msg" is not empty
                        for wait_msg in settings.CLIENTS_CONNECTED[0]["wait_msg"]:
                            if wait_msg["id"] == frame["id"]:
                                settings.CLIENTS_CONNECTED[0]["wait_msg"].remove(wait_msg)