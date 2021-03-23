# GameRadar_GUI
The GUI part of the GameRadar Framework

# Setup
Python 3.7
``pip install -r requirements.txt``

Setup config.ini
```
[server]
ip = 127.0.0.1
port = 1337
```

- ip/port specifies the address on which the GUI is waiting for connections

# Development
This part of the framework provides the GUI and places markers on a map based on the information that is sent from a datagrabber.
To add other games, add their maps into the images/games/gamename/mapimage directory.

Example Data:

```{"game": "huntshowdown", "map": "Bayou", "map_size": [3000, 3000], "objects": [{"type": "self", "x": 1670, "y": 473, "rotation": 75}, {"type": "friend", "x": 2292, "y": 1590, "rotation": 248}, {"type": "enemy", "x": 2171, "y": 2247, "rotation": 254}, {"type": "enemy", "x": 933, "y": 93, "rotation": 231, "carrier": true}, {"type": "extract", "x": 0, "y": 1500}, {"type": "extract", "x": 3000, "y": 1500}, {"type": "extract", "x": 1500, "y": 0}, {"type": "extract", "x": 1500, "y": 3000}, {"type": "target", "x": 1216, "y": 2473}, {"type": "supply", "x": 850, "y": 198}]}```

(Check the client_poc.py to see how the data is structured that the GUI expects.)

PRs and Feature requests welcome!

# Known Issues
Performance! This tool is written in Python and every image update is done with Numpy, PIL, or OpenCV. With the PoC
Client I reach refresh rates of 200ms, which should be enough in the most cases.
