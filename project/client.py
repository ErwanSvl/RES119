# -*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import socerr
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

s = socerr.socerr(socket.AF_INET, socket.SOCK_DGRAM, settings.ERROR_RATE)
adress = (settings.HOST, settings.PORT)

dic = {}
dic["adress"] = adress
dic["stop_flag"] = None
dic["timer"] = None
dic["username"] = "server"
dic["wait_msg"] = []
dic["zone"] = 0
dic["id"] = 0

settings.CLIENTS_CONNECTED.append(dic)

while not connected:
    username = connection.connectionRequest(s, adress, current_id)
    buf, adresse = s.recvfrom(settings.FRAME_LENGTH)
    frame_manager.defuseTimer(s, settings.CLIENTS_CONNECTED[0]["adress"])
    frame = frame_manager.decode_frame(buf)
    frame_manager.print_frame(frame)
    if frame["ack_state"] == 1:
        connected = True
    elif frame["error_state"] == 1:
        print "Echec de la connexion : votre login est déjà utilisé."
    elif frame["error_state"] == 2:
        print "Echec de la connexion : trop de clients connectés."


print "Connected\n"

while(settings.POWER_ON):
    rlist, _, _ = select.select([sys.stdin, s], [], [])
    for event in rlist:
        if isinstance(event, file):  # The user is writing a message
            msg = sys.stdin.readline()
            if settings.POWER_ON:
                # Incremente the ID before sending
                current_id = frame_manager.incremente_id(current_id)
                if msg[0] == "!":
                    if msg[0:len(msg) - 1] == "!quit":
                        print "Send deconnection request"
                        buf = frame_manager.encode_frame(
                            current_id, 0, username, 0, 2, 0, 0, "")
                        frame_manager.send_frame(s, adress, buf)
                        frame_manager.wait_ack(adress, s, buf)
                    else:
                        print "Error : la commande saisie est invalide, les commandes sont appelées via un '!' en début de message"
                else:
                    # The client is already waiting an ack
                    if settings.CLIENTS_CONNECTED[0]["timer"] != None and settings.CLIENTS_CONNECTED[0]["timer"].is_working:
                        settings.CLIENTS_CONNECTED[0]["wait_msg"].append(buf)
                    else:
                        buf = frame_manager.encode_frame(
                            current_id, 0, username, 0, 0, 0, 0, msg[0:len(msg) - 1])
                        frame_manager.send_frame(s, adress, buf)
                        frame_manager.wait_ack(adress, s, buf)

        else:  # The user receiving a message
            # decoding the message
            buf, adress = s.recvfrom(settings.FRAME_LENGTH)
            frame = frame_manager.decode_frame(buf)

            # detect the message type
            if frame["type"] == 0:  # Data frame
                if frame["zone"] == 0:  # Public canal
                    if frame["state"] == 0:  # Default (Message)
                        frame_manager.print_frame(frame)
                        # Send an ack frame to the server
                        frame_manager.send_ack(
                            settings.CLIENTS_CONNECTED[0]["adress"], s, frame)
                        print frame["username"]+" : "+frame["data"]
                    elif frame["state"] == 2:  # Deconnection
                        frame_manager.defuseTimer(s, adress)
                        print "Good bye !"
                        s.close()
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
                frame_manager.defuseTimer(
                    s, settings.CLIENTS_CONNECTED[0]["adress"])
