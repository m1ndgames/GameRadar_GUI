import configparser
import string
from threading import Thread
import PySimpleGUI as Gui
from imagehandler import ImageHandler
from server import RadarServer
import random


class Radar:
    def __init__(self):
        super().__init__()
        # Init variables
        self.version = '0.1a'
        self.config = configparser.ConfigParser()
        self.imagehandler = ImageHandler(self)
        self.server = RadarServer(self)
        self.setup_done = False
        self.stopthreads = False
        self.game = None
        self.mapfile = None

    def setup(self):
        self.config.read('config.ini')

        # Start server_thread
        server_thread = Thread(target=self.server.run)
        server_thread.setDaemon(True)
        server_thread.start()

        #time.sleep(1)

        # Start mapgen_thread
        mapgen_thread = Thread(target=self.imagehandler.run)
        mapgen_thread.setDaemon(True)
        mapgen_thread.start()

        self.setup_done = True

    def run(self):
        # Run setup routine
        if not self.setup_done:
            self.setup()

        # GUI

        # Set theme
        Gui.theme('DarkAmber')

        # Create the layout
        layout = [
            [Gui.Image(data=self.imagedata, key='map')]
        ]

        # Create the window
        random_title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        window = Gui.Window(title=random_title, no_titlebar=True, layout=layout, finalize=True, keep_on_top=True, grab_anywhere=True)

        # Run GUI
        while True:
            event, values = window.read(timeout=500)
            if event == Gui.WIN_CLOSED:
                break

            window.Element('map').Update(data=self.imagedata)
            window.refresh()

        self.stopthreads = True
        window.close()
