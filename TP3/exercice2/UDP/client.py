#-*- coding: utf-8 -*-

import socket, sys, getopt, os, time

try :
	opts, args = getopt.getopt(sys.argv[1:], "a:p:", ["adresse=", "port="])

except getopt.GetoptError as err :
	print "not properly used - print the options\n\n"
	sys.exit()

HOST = "localhost"
PORT = 1212

for opt, arg in opts :
	if opt in ("-a", "--adresse") :
		HOST = arg
	if opt in ("-p", "--port") :
		PORT = int(arg)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); # init protocol UDP
s.sendto("new_client_start", (HOST,PORT))
print "Connected\n"


com_ok = True
childPID = os.fork()

while(com_ok) :
	if childPID == 0 :
		rec, adresse = s.recvfrom(50)
		print "----- > "+str(rec)

	else :
		msg = raw_input()
		
		if msg == "!q":
			s.sendto("disconnected_client", (HOST, PORT))
			os.kill(childPID, 9)
			com_ok = False
		else:
			s.sendto(msg, (HOST, PORT))

print "Disconnected"
