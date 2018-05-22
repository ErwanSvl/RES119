#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import socket
import sys
import getopt
import os

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init socket

s.connect((SERVER_HOST, SERVER_PORT))  # connection to the server

sig = s.recv(50)
if sig != "start":
    print "Bad sig"
    sys.exit(2)
print "Vous pouvez commencer à tchatter : "

pid = os.fork()

message = ""
if pid == 0:  # C'est le fils
    while message != "exit":
        message = raw_input()
        s.send(message)
else:
    while message != "exit":
        message = s.recv(50)
        print message

print("Bye bye")
s.close()
sys.exit(0)