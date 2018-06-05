#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import frame_manager
import settings
import threading

#mutex = threading.Lock()


def connectionRequest(socket, adress, _id):
    """ Client connect to the server """
    print "Entrez votre nom d'utilisateur :"
    username = raw_input()
    username = username.strip()
    usernameNoSpace = username

    # Verify that username is shorter than or equal to 10 characters and longer than 0
    while(len(username) > 10) or (len(username) < 1):
        print "Le nombre de charactères doit être compris entre 1 et 10 :"
        username = raw_input()
        for i in range(10-len(username)):
            username += " "

    # Encode the frame before sending
    buf = frame_manager.encode_frame(_id, 0, username, 0, 1, 0, 0, "")
    # Send the encoding frame
    frame_manager.send_frame(socket, adress, buf)
    return usernameNoSpace


def connectionAnswer(socket, adress, username, id_server):

    is_exist = False
    for client in settings.CLIENTS_CONNECTED:
        if client["adress"] == adress:  # The connection is a reemission, the client already exist
            is_exist = True

    # Number max is reached
    if not is_exist and len(settings.CLIENTS_CONNECTED) == settings.MAX_CLIENTS:
        buf = frame_manager.encode_frame(id_server, 0, "server", 0, 1, 2, 2, "")
        frame_manager.send_frame_without_ack(socket, adress, buf)
        return frame_manager.incremente_id(id_server)

    if not is_exist:
        for client in settings.CLIENTS_CONNECTED:  # Verify the username is not used
            if username == client["username"]:
                buf = frame_manager.encode_frame(
                    id_server, 0, "server", 0, 1, 2, 1, "")
                socket.sendto(buf, adress)                
                return frame_manager.incremente_id(id_server)

    #mutex.acquire()
    #try:
        if not is_exist:
            new_client = {}
            new_client["username"] = username
            new_client["adress"] = adress
            new_client["id"] = id_server
            new_client["timer"] = None
            new_client["stop_flag"] = None
            new_client["nb_try"] = 0
            new_client["wait_msg"] = []

            settings.CLIENTS_CONNECTED.append(
                new_client)  # This is a new client
    #finally:
        #mutex.release()

    # Send a message to the other client in the channel
    msg = "L'utilisateur " + username + " s'est connecté"
    msg_buf = frame_manager.encode_frame(
        id_server, 0, "server", 0, 0, 0, 0, msg)
    id_server = frame_manager.send_frame_public(
        socket, adress, msg_buf, id_server)

    buf = frame_manager.encode_frame(id_server, 0, "server", 0, 1, 1, 0, "")
    frame_manager.send_frame_without_ack(socket, adress, buf)

    return id_server

def deconnectionAnswer(socket, adress, username, id_client, id_server):
    if settings.INFO:
        print "Envoie la réponse à la demande de déconnexion"
    for client in settings.CLIENTS_CONNECTED:  # Search and remove the client which want to disconnect
        if adress == client["adress"]:
            removeClient(adress)

            # Send a message to the other client in the channel
            msg = "L'utilisateur " + username + " s'est déconnecté"
            buf = frame_manager.encode_frame(
                id_server, 0, "server", 0, 0, 0, 0, msg)
            id_server = frame_manager.send_frame_public(
                socket, adress, buf, id_server)

    buf = frame_manager.encode_frame(
    id_client, 0, "server", 0, 2, 1, 0, "")
    socket.sendto(buf, adress)
    return id_server


def removeClient(adress):
    #mutex.acquire()
    #try:
        for client in settings.CLIENTS_CONNECTED:  # Search and remove the client which want to disconnect
            if adress == client["adress"]:
                settings.CLIENTS_CONNECTED.remove(client)
    #finally:
        #mutex.release()
