# -*- coding : utf-8 -*-
import socket, sys, os

# Program's parameters
HOST = "localhost"  # @IP host (0.0.0.0)
PORT = 1212  # Port where informations will be send and received
com_ok = True

# Socket init
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

entry = [s]
adress_client = []
msg, adress = s.recvfrom(30)
adress_client.append(adress)

while (len(adress_client) > 0):
    msg, adress = s.recvfrom(50)    
    if(msg == "new_client_start"):
        adress_client.append(adress)
        print adress_client
    elif(msg == "disconnected_client"):
        count = 0
        for client in adress_client:
            if(client == adress):
                rank = count
            count = count + 1
        
        for client in adress_client:
            if(client != adress):
                s.sendto("Client "+str(adress)+" is disconnected", client)
                
        del adress_client[rank]
        print adress_client
    else:
        for client in adress_client:
            if(client != adress):
                s.sendto(msg, client)

print "Communication closed"
