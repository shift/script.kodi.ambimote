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

		if useLegacyApi:
			capture.waitForCaptureStateChangeEvent(10)
			
		pixels = capture.getImage(1000)

		red = [];
		green = [];
		blue = [];

		for y in range(height):
			row = width * y * 4
			for x in range(width):
				red.append(pixels[row + x * 4 + 2]);
				green.append(pixels[row + x * 4 + 1]);
				blue.append(pixels[row + x * 4]);


#		red = (sum(red)/len(red));
#		green = (sum(green)/len(green));
#		blue = (sum(blue)/len(blue));

		packetArray = "%s,%s,%s" % (red,green,blue)

		try:			
			send_to_device(s,packetArray)
		except:
			print "Caught exception socket.error"

s.close()

if ( __name__ == "__main__" ):

	player_monitor = PlayerMonitor()

	try:
		capture.getCaptureState()
	except AttributeError:
		useLegacyApi = False
