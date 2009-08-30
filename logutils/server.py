from __future__ import print_function

import cPickle
import sys
import logging
import logging.handlers
import socket
import SocketServer
import struct
from datetime import datetime, timedelta

try:
    from yalib.logutils import ColorFormatter
    ColorFormatter._color = 'color'
except ImportError:
    from logging import Formatter as ColorFormatter
    ColorFormatter._color = 'mono'

class InvalidLogRecordError(Exception):
    pass

INVALID_RECORD_REPORTING_THRESHOLD = timedelta(seconds=15)

class LogRecordDatagramHandler(SocketServer.BaseRequestHandler):
    def unPickle(self, data):
        try:
            return cPickle.loads(data)
        except Exception, error:
            raise InvalidLogRecordError('failed unpickling record: %s' % (error,))

    def handle(self):
        raw_data = self.request[0]
        pickled_buffer = self.extractPickle(raw_data)
        obj = self.unPickle(pickled_buffer)
        record = logging.makeLogRecord(obj)
        self.handleLogRecord(record)

    def extractPickle(self, raw_data):
        length, pickled_buffer = raw_data[0:4], raw_data[4:]
        length = struct.unpack(">L", length)[0]
        if len(pickled_buffer) != length:
            raise InvalidLogRecordError('bad pickle length (expected %d, got %d)' % (length, len(pickled_buffer)))
        return pickled_buffer

    def handleLogRecord(self, record):
        logger = logging.getLogger(record.name)
        logger.handle(record)

class LogRecordDatagramServer(SocketServer.UDPServer):
    allow_reuse_address = 1
    def __init__(self, server_address=('0.0.0.0', logging.handlers.DEFAULT_UDP_LOGGING_PORT), bind_and_activate=True):
        SocketServer.UDPServer.__init__(self, server_address, LogRecordDatagramHandler, bind_and_activate)
        self.last_reported_error = datetime.now() - INVALID_RECORD_REPORTING_THRESHOLD
    def handle_error(self, request, client_address):
        error, error_type = sys.exc_value, sys.exc_type
        if error_type is InvalidLogRecordError:
            if self.last_reported_error + INVALID_RECORD_REPORTING_THRESHOLD < datetime.now():
                self.last_reported_error = datetime.now()
                logging.getLogger().warning("%s: %s" % (client_address[0], error))
        SocketServer.UDPServer.handle_error(self, request, client_address)

def _main(datefmt='%Y%m%d-%H%M%S', fmt='%(levelname)-8s %(message)s',
          server_address=('0.0.0.0', logging.handlers.DEFAULT_UDP_LOGGING_PORT)):
    logging.getLogger().setLevel(1)
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter(datefmt=datefmt, fmt=fmt))
    handler.setLevel(1)
    logging.getLogger().addHandler(handler)
    print("[logserver at %s; %s]" % ('%s:%s' % server_address, ColorFormatter._color))
    try:
        LogRecordDatagramServer(server_address).serve_forever()
    except KeyboardInterrupt:
        pass
    except socket.error, error:
        if error.errno != errno.EADDRINUSE:
            raise
        print('Already running (EADDRINUSE)')

def main(argv):
    # TODO: add argument parsing?
    _main()

if __name__ == "__main__":
    main(sys.argv)

