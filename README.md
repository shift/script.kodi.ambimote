# KODI AmbiMote (script.kodi.ambimote)

*NOTE*: This was hacked together over a couple of hours, more of a proof of
        concept than anything else. It is not meant for the general public.

## Background

I got a Pimoroni Mote Kit for Christmas, needed something to do with them.
Please check your Mote Sticks are all working before connecting them to your
TV. I found one of my sticks has 3 dead LEDs :'(.

## Known Issues

 * No configurable option for the IP address of the server component.
 * Android &mdash; requires hardware acceleration to be disabled to allow the
   capture code to retrieve the screen colours.
 * UDP Datagrams could be packed/unpacked in a better fashion.

## Requirements

Hardware:
 * [Pimoroni Mote Host](https://shop.pimoroni.de/products/mote)
 * [Pimoroni Mote Stick](https://shop.pimoroni.de/products/mote)
 * Cables to connect the Host to the Sticks.
 * Raspberry Pi / ODROID C2 or other embedded Linux to run the server service.

## Setup

Currently the IP address is hardcoded on line 17 of `addon.py`, please change
this if your Python server isn't running at `192.168.1.148`.

The server component can be found under `server/` along with its own
[documentation](server/README.md) for setup.

This addon will change the color of your Pimoroni Mote Sticks to match the
currently playing video.

# Credits

Based upon the work carried out here [kodi-lifx](http://www.blinkingled.be/lifx-plugin-for-kodi/)
