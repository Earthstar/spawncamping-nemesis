#!/usr/bin/python2
# Initially written by Ricardo Pascal
# http://voorloopnul.com/blog/a-python-proxy-in-less-than-100-lines-of-code/
# Distributed over IDC(I Don't Care) license
# Significantly reworked by Andres Erbsen <andres@krutt.org>

import logging
import time
import socket
import select
import sys

TIMELIMIT = 1.
REFRESHRATE = 1.
TCP_BACKLOG = 200
SIZELIMIT=1<<12

def pL(*args):
    return ' '.join(str(s) for s in args)

class TCPFilter:
    input_list = []
    channel = {}
    timeout = {} # client-side sockets have time limits
    bytes_remaining = {}

    def __init__(self, (host, port), forward_to):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(TCP_BACKLOG)
	self.forward_to = forward_to

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            for sock in select.select(self.input_list, [], [], REFRESHRATE)[0]:
                if sock == self.server:
                    self.on_accept()
                else:
                    bs = sock.recv(1+SIZELIMIT)
                    if bs:
                        self.on_recv(sock, bs)
                    else:
                        self.on_close(sock)

    def on_accept(self):
        sock, clientaddr = self.server.accept()
        logging.info(pL(clientaddr, "has connected"))
        try:
            forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            forward.connect(self.forward_to)
        except Exception, e:
            logging.warn("The filtered service seems to be down; dropping client")
            logging.warn(e)
            sock.close()
            return
        self.input_list.append(sock)
        self.input_list.append(forward)
        self.channel[sock] = forward
        self.channel[forward] = sock
        self.timeout[sock] = time.time() + TIMELIMIT
        self.bytes_remaining[sock] = SIZELIMIT

    def on_close(self, sock):
        logging.info(pL(sock.getpeername(), "has disconnected"))
        self.channel[sock].close()
        sock.close()
        self.input_list.remove(self.channel[sock])
        self.input_list.remove(sock)
        if sock in self.timeout: del self.timeout[sock]
        if sock in self.bytes_remaining: del self.bytes_remaining[sock]
        del self.channel[self.channel[sock]]
        del self.channel[sock]

    def on_recv(self, sock, bs):
        details = ['from', sock.getpeername(), 'to',
self.channel[sock].getpeername(),repr(bs), '-', len(bs), 'bytes of', self.bytes_remaining.get(sock, 1e333), 'remaining']
        if (sock in self.timeout and any([
            len(bs) > self.bytes_remaining.get(sock, 1e333),
            'AAAAA' in bs.upper(),
            'SELECT' in bs.upper(),
            'DROP' in bs.upper(),
            'OR' in bs.upper(),
            'TABLE' in bs.upper(),
            '--' in bs.upper()
            #'*' in bs.upper()
                ])):
            logging.info(pL(*(details + ['(rejected)'])))
            self.on_close(sock)
        else:
            logging.info(pL(*details))
	    if sock in self.bytes_remaining: self.bytes_remaining[sock] -= len(bs)
            self.channel[sock].send(bs)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print ('USAGE: ' +sys.argv[0]+ ': listen_host listen_port target_host target_port')
        exit()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')
    server = TCPFilter((sys.argv[1], int(sys.argv[2])), (sys.argv[3],int(sys.argv[4])))
    try:
        server.main_loop()
    except KeyboardInterrupt:
        logging.critical("Ctrl C - Stopping TCPFilter")
        sys.exit(1)
