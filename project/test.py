#/bin/python
#-*- coding : utf-8 -*-

import ctypes
import struct
import argparse

"""                                                       Exemple de message """

""" Initialise le Buffer à 190 bits """
buf = ctypes.create_string_buffer(190);

""" Donne la taille de la data : 160 octets ici """
data = 160;

""" Le message à transmettre de taille <data> """
msg = "je m'appelle killian";

""" Fais un struct """
struct.pack_into('H10sHB'+str(data)+'s', buf, 0, 0b000000000000010, 'toto', 0, 0b00000000, msg);
