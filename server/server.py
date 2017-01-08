#!/usr/bin/env python3
"""AmbiMote UDP Server."""
import argparse
import sys
import asyncio
import struct
from base64 import b16encode
from mote import Mote

mote = Mote()

mote.configure_channel(1, 16, True)
mote.configure_channel(2, 16, True)
mote.configure_channel(3, 16, True)
mote.configure_channel(4, 16, True)


try:
    import signal
except ImportError:
    signal = None

class UdpAmbiMoteProtocol:
    pix_no = 0
    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport

    @staticmethod
    def parse_rgb(i):
        i = str(i).replace('b"','').replace('"','')
        return int(i[0:2], 16), int(i[2:4], 16), int(i[4:6], 16)

    def pix_inc(self):
        if self.pix_no == 15:
            self.pix_no = 0
        else:
            self.pix_no += 1
        return self.pix_no

    def datagram_received(self, data, addr):
        # This needs to die
        data = str(data)
        data = data.replace(' ','').replace("[", '').replace("'",'').replace("]",'').split(',')

        # We get a 32x32 array of RGB
        for pixel in data[0:16]:
            r, g, b = self.parse_rgb(pixel) 
            mote.set_pixel(1, self.pix_inc(), int(r), int(g), int(b))
        for pixel in data[16:32]:
            r, g, b = self.parse_rgb(pixel) 
            mote.set_pixel(2, self.pix_inc(), int(r), int(g), int(b))
        for pixel in data[992:1008]:
            r, g, b = self.parse_rgb(pixel) 
            mote.set_pixel(3, self.pix_inc(), int(r), int(g), int(b))
        for pixel in data[1009:1024]:
            r, g, b = self.parse_rgb(pixel) 
            mote.set_pixel(4, self.pix_inc(), int(r), int(g), int(b))
        mote.show()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)


def start_server(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        UdpAmbiMoteProtocol, local_addr=addr))
    transport, server = loop.run_until_complete(t)
    return transport


ARGS = argparse.ArgumentParser(description="AmbiMote UDP Server.")
ARGS.add_argument(
    '--host', action="store", dest='host',
    default='0.0.0.0', help='Host name')
ARGS.add_argument(
    '--port', action="store", dest='port',
    default=9642, type=int, help='Port number')


if __name__ == '__main__':
    args = ARGS.parse_args()
    if ':' in args.host:
        args.host, port = args.host.split(':', 1)
        args.port = int(port)

    else:
        loop = asyncio.get_event_loop()
        if signal is not None:
            loop.add_signal_handler(signal.SIGINT, loop.stop)

        server = start_server(loop, (args.host, args.port))
        try:
            loop.run_forever()
        finally:
            if '--server' in sys.argv:
                server.close()
            loop.close()
