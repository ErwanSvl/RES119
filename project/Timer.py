from threading import Thread, Event
import frame_manager
import settings
import connection
import socket
import sys

class Timer(Thread):
    def __init__(self, event, duration, try_max, buf, socket, adress):
        Thread.__init__(self)
        self.stopped = event
        self.nb_try = 1
        self.duration = duration
        self.try_max = try_max
        self.buf = buf
        self.socket = socket
        self.adress = adress
        self.is_working = True

    def run(self):

        while not self.stopped.wait(self.duration) and self.nb_try < self.try_max:
            if settings.INFO:
                print "ACK perdu, reemission pour la " + str(self.nb_try) + " fois"
            self.socket.sendto(self.buf, self.adress)
            self.nb_try += 1
        if self.nb_try >= self.try_max: # Too much retry, give up
            connection.removeClient(self.adress)
            print "Error : destinaire injoingnable, abandon"
            settings.POWER_ON = False # Diffuse the main loop
        self.is_working = False


    def getID(self):
        """ Return the ID of the data frame that timer is waiting for the same ID ack frame """
        frame = frame_manager.decode_frame(self.buf)
        return frame["id"]
