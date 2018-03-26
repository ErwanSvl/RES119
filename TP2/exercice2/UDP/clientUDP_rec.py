#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import socket
import sys
import getopt

OPT_SHORT = 'hp:m:'
OPT_LONG = ['help', 'port=', 'message=']
SERVER_HOST = 'localhost'
SERVER_PORT = 1212
MESSAGE = 'Hello world !'


def printHelp():
    print "—  -h /--help : afficher l'aide"
    print "—  -p /--port : spécifier le numéro de port serveur"


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
        SERVER_PORT = arg
    elif opt in ('-m', '--message'):
        MESSAGE = arg

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # init socket

s.connect((SERVER_HOST, SERVER_PORT))  # connection to the server

# sending a message to the server
s.sendto(MESSAGE, (SERVER_HOST, SERVER_PORT))
message, adress = s.recvfrom(50)
print "Message reçut : " + message + " de : " + str(adress)
s.close()
