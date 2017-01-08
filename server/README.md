# AmbiMote Python Server

## Requirements

Hardware:
 * [Pimoroni Mote Host](https://shop.pimoroni.de/products/mote)
 * [Pimoroni Mote Stick](https://shop.pimoroni.de/products/mote)
 * Cables to connect the Host to the Sticks.

Software:
 * Python 3
 * pip

## Installation

```bash
pip3 install -r requirements.txt
```

## Running

Add the user which the server runs as to the `uucp` group, you
check the group required by checking the group of the `/dev/ttyACM0` device
or depending on which distribution is used this may be different.

```bash
python3 server.py
```

If you want to skip adding to this group, you will need to run as root or via
`sudo`.

## Stick Locations

Locations are hardcoded currently to be:

```
 1----       2----
 _________________
|                 |
|                 |
|                 |
| _______________ |
 3----       4----
```


