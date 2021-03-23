import configparser
import ctypes
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
        self.version = '0.2a'
        self.config = configparser.ConfigParser()
        self.imagehandler = ImageHandler(self)
        self.server = RadarServer(self)
        self.setup_done = False
        self.stopthreads = False
        self.game = None
        self.mapfile = None
        self.zoom_level = 50

    def setup(self):
        ctypes.windll.user32.SetProcessDPIAware()

        self.config.read('config.ini')

        # Start server_thread
        server_thread = Thread(target=self.server.run)
        server_thread.setDaemon(True)
        server_thread.start()

        # Start mapgen_thread
        mapgen_thread = Thread(target=self.imagehandler.run)
        mapgen_thread.setDaemon(True)
        mapgen_thread.start()

        self.setup_done = True

    def run(self):
        # Run setup routine
        if not self.setup_done:
            self.setup()

        # Set theme
        Gui.theme('DarkAmber')

        # Create the layout
        layout = [
            [Gui.Image(data=self.imagedata, key='map')],
            [Gui.Button('Quit'), Gui.Button('-'), Gui.Button(str(self.zoom_level) + "%", key='reset_zoom'), Gui.Button('+')]
        ]

        # Create the window
        random_title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        window = Gui.Window(title=random_title, no_titlebar=True, layout=layout, finalize=True, keep_on_top=True, grab_anywhere=True, return_keyboard_events=True)
        window['map'].bind('<MouseWheel>', 'MouseWheel')
        window.TKroot.minsize(100, 100)
        window.TKroot.maxsize(900, 1000)

        # Run GUI
        while True:
            event, values = window.read(timeout=100)
            if event == Gui.WIN_CLOSED or event == 'Quit':
                break
            elif event == '+' or event == 'MouseWheel:Up':
                if self.zoom_level >= 100:
                    self.zoom_level = 100
                else:
                    self.zoom_level = self.zoom_level + 10

                window.Element('reset_zoom').Update(text=[str(self.zoom_level) + "%"])
            elif event == '-' or event == 'MouseWheel:Down':
                if self.zoom_level <= 0:
                    self.zoom_level = 0
                else:
                    self.zoom_level = self.zoom_level - 10
                window.Element('reset_zoom').Update(text=[str(self.zoom_level) + "%"])

            elif event == 'reset_zoom':
                window.Element('reset_zoom').Update(text=['50%'])
                self.zoom_level = 50

            window.Element('map').Update(data=self.imagedata)
            window.refresh()

        self.stopthreads = True
        window.close()
