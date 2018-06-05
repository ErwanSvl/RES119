# -*- coding:utf-8 -*-
import argparse
import ctypes
import getopt
import os
import socket
import struct
import sys

import connection
import frame_manager
import settings
import socerr

OPT_SHORT = 'ha:p:n:e:'
OPT_LONG = ['help', 'adress=', 'port=', 'nb=', 'debug', 'info', 'errors=']


def printHelp():
    print "—  -h /--help : afficher l'aide"
    print "—  -p / --port : Choisir le port utilisé"
    print "—  -a / --adress : Choisir l'adresse utilisée"
    print "—  -n / --nb : Choisir le nombre de réémission avant abandon"
    print "—  -e / --errors : Choisir le taux d'erreurs"
    print "—  --info : afficher les logs"
    print "—  --debug : afficher les trames"


os.system('cls||clear')

try:
    opts, args = getopt.getopt(sys.argv[1:], OPT_SHORT, OPT_LONG)
except getopt.GetoptError as err:
    print "Les options ne sont pas correctes : "
    printHelp()
    sys.exit()
for opt, arg in opts:
    if opt in ('-h', '--help'):
        printHelp()
        sys.exit()
    elif opt in ('', '--info'):
        settings.INFO = True
    elif opt in ('', '--debug'):
        settings.DEBUG = True
    elif opt in ('-a', '--adress'):
        settings.HOST = arg
    elif opt in ('-n', '--nb'):
        settings.TRY_MAX = int(arg)
    elif opt in ('-p', '--port'):
        settings.PORT = arg
    elif opt in ('-e', '--errors'):
        settings.ERROR_RATE = int(arg)
    

POWER_ON = True
current_id = 0

if settings.INFO:
    print "Taux d'erreurs : " + str(settings.ERROR_RATE)
s = socerr.socerr(socket.AF_INET, socket.SOCK_DGRAM, settings.ERROR_RATE)
s.bind((settings.HOST, settings.PORT))

while POWER_ON:
    buf, adress = s.recvfrom(settings.FRAME_LENGTH)
    frame = frame_manager.decode_frame(buf)
    if settings.DEBUG:
        frame_manager.print_frame(frame)
    if frame["type"] == 0:  # Data frame
        if frame["zone"] == 0:  # Public canal
            if frame["state"] == 0:  # Default (Message)
                for client in settings.CLIENTS_CONNECTED:
                    if client["adress"] == adress:  # Find the sender
                        frame_manager.send_ack(adress, s, frame)
                        # if the ID is the same : this message is a reemission
                        if client["id"] != frame["id"]:
                            client["id"] = frame["id"]  # Update the client ID
                            current_id = frame_manager.send_frame_public(
                                s, adress, buf, current_id)
            elif frame["state"] == 1:  # Connection
                connection.connectionAnswer(
                    s, adress, frame["username"], frame["id"])
            elif frame["state"] == 2:  # Deconnection
                current_id = connection.deconnectionAnswer(
                    s, adress, frame["username"], frame["id"], current_id)
            elif frame["state"] == 3:  # Server command
                if frame["data"] == "who":
                    frame_manager.send_ack(adress, s, frame)
                    current_id = frame_manager.send_list(s, adress, current_id)
                else:
                    if settings.INFO:
                        print "Cette commande n'est pas géré par le serveur"
            else:  # Bad entry
                if settings.INFO:
                    print "Bad Entry"
        elif frame["zone"] == 1:  # Centralized private canal
            print "Not implemented yet"
        elif frame["zone"] == 2:  # Decentralized private canal
            print "Not implemented yet"
        else:  # Bad entry zone parameter
            if settings.INFO:
                print "Bad Entry"
    else:  # Ack frame
        frame_manager.defuseTimer(s, adress)
