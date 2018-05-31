from socket import socket
import random

class socerr(socket):

    def __init__(self, domain, transport, rate):
        self._sock = socket(domain, transport)
        self.error = rate
        self.n = 1

    def sendto(self, *p):
        if self.error >= 0:
            test = random.randint(1,100)
            if test > self.error:
                return self._sock.sendto(*p)
            else :
                print ("** LOSS **")
        else:
            if self.n == -self.error :
                print ("** LOSS **")
                self.n = 1
            else:
                self.n += 1
                return self._sock.sendto(*p)

    def recvfrom(self, *p):
        return self._sock.recvfrom(*p)
