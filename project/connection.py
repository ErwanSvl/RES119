#-*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import frame_manager
import settings


def connectionRequest(socket, adress, _id):
    """ Client connect to the server """
    print "Entrez votre nom d'utilisateur :"
    username = raw_input()
    username = username.strip()
    usernameNoSpace = username

    # Verify that username is shorter than or equal to 10 characters and longer than 0
    while(len(username) > 10) or (len(username) < 1):
        print username
        print len(username)
        print "Le nombre de charactères doit être compris entre 1 et 10 :"
        username = raw_input()
        for i in range(10-len(username)):
            username += " "

    # Encode the frame before sending
    buf = frame_manager.encode_frame(_id, 0, username, 0, 1, 0, 0, "")
    # Send the encoding frame
    frame_manager.send_frame(socket, adress, buf)
    return usernameNoSpace


def connectionAnswer(socket, adress, username, _id):

    if len(settings.CLIENTS_CONNECTED) == settings.MAX_CLIENTS:  # Number max is reached
        buf = frame_manager.encode_frame(_id, 0, "server", 0, 1, 2, 2, "")
        frame_manager.send_frame(socket, adress, buf)
        return

    for client in settings.CLIENTS_CONNECTED:  # Verify the username is not used
        if username == client["username"]:
            buf = frame_manager.encode_frame(_id, 0, "server", 0, 1, 2, 1, "")
            frame_manager.send_frame(socket, adress, buf)
            return
    dic = {}
    dic["username"] = username
    dic["adress"] = adress
    dic["id"] = _id
    dic["timer"] = None
    dic["nb_try"] = 0
    dic["wait_msg"] = []
    settings.CLIENTS_CONNECTED.append(dic)

    buf = frame_manager.encode_frame(_id, 0, "server", 0, 1, 1, 0, "")
    frame_manager.send_frame(socket, adress, buf)


def deconnectionAnswer(socket, adress, username, id_client, id_server):

    for client in settings.CLIENTS_CONNECTED: # Search and remove the client which want to disconnect
        if adress == client["adress"]:
            settings.CLIENTS_CONNECTED.remove(client)
            buf = frame_manager.encode_frame(
                id_client, 0, "server", 0, 2, 1, 0, "")
            frame_manager.send_frame(socket, adress, buf)

    msg = "L'utilisateur " + username + " s'est déconnecté"
    buf = frame_manager.encode_frame(id_server, 0, "server", 0, 0, 0, 0, msg)
    id_server = frame_manager.send_frame_public(socket, adress, buf, id_server)
    return id_server
