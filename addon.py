import xbmc
import xbmcaddon
import xbmcgui
import os

import socket
import sys
import binascii
import colorsys
import struct

from binascii import unhexlify

addon = xbmcaddon.Addon();

def send_to_device(socket,message):
    socket.sendto(message,("192.168.1.148", 9642));


bulbCount = int(addon.getSetting("bulbcount"));
refreshRate = int(addon.getSetting("refreshrate"));
min_brightness = int(addon.getSetting("minbrightness"))*655;

useLegacyApi   = True
capture = xbmc.RenderCapture()

if useLegacyApi:
	capture.capture(32, 32, xbmc.CAPTURE_FLAG_CONTINUOUS)

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

class PlayerMonitor( xbmc.Player ):
	def __init__( self, *args, **kwargs ):
		xbmc.Player.__init__( self )

	def onPlayBackStarted( self ):
		if not useLegacyApi:
			capture.capture(32, 32)


while not xbmc.abortRequested:
	xbmc.sleep(refreshRate)
	if capture.getCaptureState() == xbmc.CAPTURE_STATE_DONE:
		width = capture.getWidth();
		height = capture.getHeight();
		pixels = capture.getImage(1000);
                print("Width: %s, Height: %s" % (width, height))
		if useLegacyApi:
			capture.waitForCaptureStateChangeEvent(10)
			
		pixels = capture.getImage(1000)

		reds = [];
		greens = [];
		blues = [];
                leds = []
                rgb = (0,0,0)
		for y in range(height):
			row = width * y * 4
			for x in range(width):
                                rgb = (pixels[row + x * 4 + 2], pixels[row + x * 4 + 1], pixels[row + x * 4])
                                leds.append(struct.pack('BBB',*rgb).encode('hex'))
                print(len(str(leds)))
                try:			
                    send_to_device(s,str(leds))
                except:
                    print "Caught exception socket.error"

s.close()

if ( __name__ == "__main__" ):

	player_monitor = PlayerMonitor()

	try:
		capture.getCaptureState()
	except AttributeError:
		useLegacyApi = False
