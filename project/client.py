# -*- coding:utf-8 -*-
import argparse
import ctypes
import getopt
import os
import random
import select
import socket
import struct
import sys
from threading import Event, Thread

import connection
import frame_manager
import settings
import socerr
from Timer import Timer

OPT_SHORT = 'h'
OPT_LONG = ['debug', 'info']


def printHelp():
    print "—  -h /--help : afficher l'aide"
    print "—  --info : afficher les logs"
    print "—  --debug : afficher les trames"


os.system('cls||clear')

try:
    opts, args = getopt.getopt(sys.argv[1:], OPT_SHORT, OPT_LONG)
except getopt.GetoptError as err:
    print "Les options ne sont pas correctes : "
    printHelp()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        printHelp()
        sys.exit()
    elif opt in ('', '--info'):
        settings.INFO = True
    elif opt in ('', '--debug'):
        settings.DEBUG = True

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
dic["id"] = -1

settings.CLIENTS_CONNECTED.append(dic)

while not connected:
    username = connection.connectionRequest(s, adress, current_id)
    buf, adress = s.recvfrom(settings.FRAME_LENGTH)
    frame_manager.defuseTimer(s, settings.CLIENTS_CONNECTED[0]["adress"])
    frame = frame_manager.decode_frame(buf)
    if settings.DEBUG:
        frame_manager.print_frame(frame)
    if frame["ack_state"] == 1:
        connected = True
    elif frame["error_state"] == 1:
        print "Echec de la connexion : votre login est déjà utilisé."
    elif frame["error_state"] == 2:
        print "Echec de la connexion : trop de clients connectés."


print "Vous êtes connecté.\n"

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
                        if settings.INFO:
                            print "Envoie d'une requete de déconnexion"
                        buf = frame_manager.encode_frame(
                            current_id, 0, username, 0, 2, 0, 0, "")
                        frame_manager.send_frame(s, adress, buf)
                    elif msg[0:len(msg) - 1] == "!who":
                        if settings.INFO:
                            print "Envoie d'une demande de la liste des utilisateurs"
                        buf = frame_manager.encode_frame(current_id, 0, username, 0, 3, 0, 0, "who")
                        frame_manager.send_frame(s, adress, buf)
                    else:
                        print "Error : la commande saisie est invalide, les commandes sont appelées via un '!' en début de message\nLes commandes disponibles sont !who et !quit"
                else:
                    buf = frame_manager.encode_frame(
                        current_id, 0, username, 0, 0, 0, 0, msg[0:len(msg) - 1])
                    frame_manager.send_frame(s, adress, buf)

        else:  # The user receiving a message
            # decoding the message
            buf, adress = s.recvfrom(settings.FRAME_LENGTH)
            frame = frame_manager.decode_frame(buf)
            if settings.DEBUG:
                frame_manager.print_frame(frame)
            # detect the message type
            if frame["type"] == 0:  # Data frame
                if frame["zone"] == 0:  # Public canal
                    if frame["state"] == 0:  # Default (Message)
                        # Send an ack frame to the server
                        frame_manager.send_ack(
                            settings.CLIENTS_CONNECTED[0]["adress"], s, frame)
                        if settings.CLIENTS_CONNECTED[0]["id"] != frame["id"]:
                            settings.CLIENTS_CONNECTED[0]["id"] = frame["id"]
                            print frame["username"]+" : "+frame["data"]
                    elif frame["state"] == 2:  # Deconnection
                        frame_manager.defuseTimer(s, adress)
                        print "Au revoir !"
                        s.close()
                        sys.exit()
                    elif frame["state"] == 3:  # Server command
                        pass
                    else:  # Bad entry
                        if settings.INFO:
                            print "Bad entry"
                elif frame["zone"] == 1:  # Centralized private canal
                    print "Not implemented yet"
                elif frame["zone"] == 2:  # Decentralized private canal
                    print "Not implemented yet"
                else:  # Bad entry zone parameter
                    if settings.INFO:
                        print "Bad entry"
            else:  # Ack frame
                frame_manager.defuseTimer(
                    s, settings.CLIENTS_CONNECTED[0]["adress"])
