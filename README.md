# GameRadar_GUI
The GUI part of the GameRadar Framework

# Setup
Python 3.7
``pip install -r requirements.txt``

Setup config.ini
```
[radar]
updatecycle = 500

[server]
ip = 127.0.0.1
port = 1337
```

- Updatecycle is the refreshrate of the Gui
- ip/port specifies the address on which the GUI is waiting for connections

# Development
This part of the framework provides the GUI and places markers on a map based on the information that is sent from a datagrabber.
To add other games, add their maps into the images/games/<game>/mapimage directory.

Check the client_poc.py to see how the data is structured that the GUI expects.

PRs and Feature requests welcome!
