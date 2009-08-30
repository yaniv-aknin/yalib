import logging.handlers
from functools import partial
from logging import Formatter, Filter, Logger
import logging
import socket

from yalib.console import colorize

class NonBlockingDatagramHandler(logging.handlers.DatagramHandler):
    "Mostly the vanilla DatagramHandler with some extra safety/non-blockingess additions"
    def __init__(self, host='127.0.0.1', port=logging.handlers.DEFAULT_UDP_LOGGING_PORT):
        logging.handlers.DatagramHandler.__init__(self, host, port)

    def makeSocket(self):
        "The DatagramHandler factory is overriden to create a non-blocking socket."
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        return sock

    def send(self, s):
        """
        Add exception handling. I've read the CPython code of sendto and am not sure it can create an exception
         on a nonblocking datagram socket, but better safe than sorry.
        """
        if self.sock is None:
            self.createSocket()
        try:
            self.sock.sendto(s, (self.host, self.port))
        except socket.error:
            self.sock.close()
            # Note: so we can call createSocket next time
            self.sock = None

class ColorFormatter(Formatter):
    SEVERITY_COLOR_THRESHOLDS = (
        (0, 'blue'),
        (10, 'cyan'),
        (20, 'green'),
        (30, 'yellow'),
        (40, 'red'),
        (50, 'magenta'),
    )
    def format(self, record):
        plain_result = Formatter.format(self, record)
        for severity_threshold, severity_color in self.SEVERITY_COLOR_THRESHOLDS:
            if record.levelno >= severity_threshold:
                color = severity_color
            else:
                break
        return colorize(plain_result, color=color)
