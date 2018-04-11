#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import socket
import sys
import getopt
import os
import select

OPT_SHORT = 'hp:'
OPT_LONG = ['help', 'port=']

HOST = 'localhost'
PORT = 1212

IS_WORKING = True


def printHelp():
    print "—  -h /--help : afficher l'aide"
    print "—  -p /--port : spécifier le numéro de port serveur"


while IS_WORKING:
    try:
        opts, args = getopt.getopt(sys.argv[1:], OPT_SHORT, OPT_LONG)
    except getopt.GetoptError as err:
        print "Les options ne sont pas correctes : "
        printHelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printHelp()
            sys.exit(2)
        elif opt in ('-p', '--port'):
            PORT = arg

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init socket

    s.bind((HOST, PORT))  # listen the port
    s.listen(10)

    clients = []
    new_clients, writable, exceptional = select.select([s], [], [], 0.05)

    for new_client in new_clients:
        socket_client, adress_clien = new_client.accept()
        clients.append(socket_client)

    writing_clients = []
    try:
        writing_clients, writable, exceptional = select.select(
            clients, [], [], 0.05)
    except select.error as e:
        print "Une erreur est survenue : " + str(e)
    else:
        for client in writing_clients:
            message = client.recv(50)
            print "Reception du message : " + message
            if message == "exit":
                IS_WORKING = False

print "Fermeture des connections."
for client in clients:
    client.close()
s.close()
