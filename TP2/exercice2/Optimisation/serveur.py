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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init socket

s.bind((HOST, PORT))  # listen the port
s.listen(10)

socket_client_em, addr_client_em = s.accept()
socket_client_em.send("premier")  # Le client est l'émetteur
message = socket_client_em.recv(50)  # parameter is message max lenght
print "Message reçus : " + message

socket_client_rec, addr_client_rec = s.accept()
socket_client_rec.send("deuxieme")  # Le client est le receveur
print "tempo"
socket_client_rec.send(message)
print "Message transmis : " + message
