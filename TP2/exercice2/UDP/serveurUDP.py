#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import socket
import sys
import getopt

OPT_SHORT = 'hp:'
OPT_LONG = ['help', 'port=']

HOST = 'localhost'
PORT = 1212


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
        PORT = arg

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # init socket

s.bind((HOST, PORT))

message_em, adress_em = s.recvfrom(50)
print "message reçut : " + message_em + " de : " + str(adress_em)

message_rec, adress_rec = s.recvfrom(50)
s.sendto(message_em, adress_rec)
print "message envoyé : " + message_em + " à : " + str(adress_rec)
