#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import socket
import sys
import getopt
import os

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
# message = socket_client_em.recv(50)  # parameter is message max lenght
print "Première connexion : " + str(addr_client_em)

socket_client_rec, addr_client_rec = s.accept()
# socket_client_rec.send(message)
print "Deuxieme connexion : " + str(addr_client_rec)

socket_client_em.send("start")
socket_client_rec.send("start")

pid = os.fork()

message = ""
if pid == 0:  # C'est le fils
    while message != "exit":
        message = socket_client_em.recv(50)
        socket_client_rec.send(message)
else:
    while message != "exit":
        message = socket_client_rec.recv(50)
        socket_client_em.send(message)

sys.exit(0)
