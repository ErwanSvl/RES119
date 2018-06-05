# -*- coding:utf-8 -*-
import ctypes
import struct
import argparse
import socket
import connection
import settings
from threading import Thread, Event
from Timer import Timer


def encode_frame(_id, _type, username, zone, state, ack_state, error_state, data):
    """ Return the buffer encoded """
    # concat id and type
    idtype = (_id << 1) + _type
    # concat state, ack_state, error_state
    state_ackSt_ackEr = (state << 6) + (ack_state << 4) + error_state
    # create the buffer
    buf = ctypes.create_string_buffer(15 + len(data))
    # fill the buffer, the data length is variable
    struct.pack_into('H10sHB' + str(len(data)) + 's', buf, 0,
                     idtype, username, zone, state_ackSt_ackEr, data)
    return buf


def send_frame(socket, adress, buf):
    """ Send a frame with parameters encoded to the server"""
    # send the buffer
    for client in settings.CLIENTS_CONNECTED:
        if client["adress"] == adress:
            # No waiting ack
            if (client["timer"] == None or not client["timer"].is_working) and len(client["wait_msg"]) == 0:
                if settings.INFO:
                    print "Envoie du message et démarrage du timer pour " + \
                        client["username"]
                socket.sendto(buf, adress)
                wait_ack(adress, socket, buf)
            else:  # Waiting ack : add to buffer
                if settings.INFO:
                    print "On attend déjà un ACK, ajout de la trame au buffer"
                client["wait_msg"].append(buf)
                if settings.INFO:
                    print_buffer()
            return


def send_frame_without_ack(socket, adress, buf):
    """ Send a frame with parameters encoded to the server"""
    # send the buffer
    for client in settings.CLIENTS_CONNECTED:
        if client["adress"] == adress:
            # There is already a waiting ack
            if (client["timer"] == None or not client["timer"].is_working) and len(client["wait_msg"]) == 0:
                socket.sendto(buf, adress)
            else:  # Send the frame and init the timer
                if settings.INFO:
                    print "On attend déjà un ACK, ajout de la trame au buffer"
                client["wait_msg"].append(buf)
                if settings.INFO:
                    print_buffer()
            return


def send_frame_public(socket, adress, buf, id_server):
    """ Send a frame with parameters encoded to all the connected clients except the sender.
    Return the final server id incremented"""
    frame = decode_frame(buf)  # the ID have to change so we need to decode
    for user in settings.CLIENTS_CONNECTED:
        updated_buf = encode_frame(id_server, frame["type"], frame["username"], frame["zone"],
                                   frame["state"], frame["ack_state"], frame["error_state"], frame["data"])
        if user["adress"] != adress:
            send_frame(socket, user["adress"], updated_buf)
            id_server = incremente_id(id_server)
    return id_server


def decode_frame(buf):
    """ Return the value of a frame received """
    data_size = len(buf) - 15
    frame = {}

    idType = struct.unpack('H', buf[0:2])[0]
    frame["id"] = idType >> 1
    frame["type"] = idType % 2

    frame["username"] = struct.unpack("10s", buf[2:12])[0]
    frame["zone"] = struct.unpack("H", buf[12:14])[0]

    state_ackSt_ackEr = struct.unpack("B", buf[14])[0]
    frame["state"] = state_ackSt_ackEr >> 6
    frame["ack_state"] = (state_ackSt_ackEr >> 4) % 4
    frame["error_state"] = state_ackSt_ackEr % 16

    frame["data"] = struct.unpack(
        str(data_size) + "s", buf[15:(15 + data_size)])[0]
    return frame


def print_frame(frame):
    print "		ID : "+str(frame["id"])
    print "		TYPE : "+str(frame["type"])
    print "		UTILISATEUR : "+str(frame["username"])
    print "		ZONE : "+str(frame["zone"])
    print "		STATE : "+str(frame["state"])
    print "		ACK STATE : "+str(frame["ack_state"])
    print "		ERREUR STATE : "+str(frame["error_state"])
    print "		DATA : "+str(frame["data"])
    print "---------------------------------------------------------"


def get_user(adress):
    for user in settings.CLIENTS_CONNECTED:
        if user["adress"] == adress:
            return user


def incremente_id(ID):
    if ID >= settings.MAX_ID:
        return 1
    else:
        return ID + 1


def send_ack(adress, socket, frame):
    buf = encode_frame(frame["id"], 1, "", 0, 0, 0, 0, "")
    socket.sendto(buf, adress)
    if settings.INFO:
        print "Envoie un ACK à " + frame["username"]


def wait_ack(adress, socket, buf):
    for client in settings.CLIENTS_CONNECTED:
        if client["adress"] == adress:
            stopFlag = Event()
            client["timer"] = Timer(
                stopFlag, settings.DURATION_TIMER, settings.TRY_MAX, buf, socket, adress)
            client["timer"].start()
            client["stop_flag"] = stopFlag


def defuseTimer(socket, adress):
    if settings.INFO:
        print "ACK reçu, timer désarmé"
    for client in settings.CLIENTS_CONNECTED:
        if client["adress"] == adress:
            client["stop_flag"].set()
            if len(client["wait_msg"]) > 0:
                if settings.INFO:
                    print "Envoie d'un message en attente"
                    print_buffer()
                # Take off the first frame of the table
                buf = client["wait_msg"].pop(0)
                socket.sendto(buf, adress)
                wait_ack(adress, socket, buf)


def print_buffer():
    for client in settings.CLIENTS_CONNECTED:
        print "\n"+str(client["username"])+" : ["
        for buf in client["wait_msg"]:
            frame = decode_frame(buf)
            print "data : "+str(frame["data"])+"/ id : "+str(frame["id"])
        print "]\n"

def send_list(socket, adress, id_server):
    message = ""
    for client in settings.CLIENTS_CONNECTED:
        message += client["username"] + ":public "
    buf = encode_frame(id_server, 0, "server", 0, 0, 0, 0, message)
    send_frame(socket, adress, buf)
    return incremente_id(id_server)