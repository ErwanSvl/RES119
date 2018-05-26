from threading import Thread, Event
import time
import frame_manager
import settings
import connection


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
            frame_manager.send_frame(self.socket, self.adress, self.buf)
            self.nb_try += 1
        if self.nbtry >= self.try_max:
            connection.removeClient(self.adress)
        self.is_working = False
