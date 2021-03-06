import socket
import json


class RadarServer:
    def __init__(self, radar=None):
        self.radar = radar
        self.radar.map = None
        self.radar.mapfile = None
        self.radar.objects = []
        self.radar.received_update = False

    def unpack_json(self, json_data):
        self.radar.objects = []
        data = json.loads(json_data)

        self.radar.game = data['game']
        self.radar.map = data['map']
        self.radar.map_size = data['map_size']

        for o in data['objects']:
            self.radar.objects.append(o)

    def run(self):
        while not self.radar.stopthreads:
            bufferSize = 1024

            # Create a datagram socket
            UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            # Bind to address and ip
            UDPServerSocket.bind((self.radar.config['server']['ip'], int(self.radar.config['server']['port'])))

            print("RadarGui v" + self.radar.version + " - https://github.com/m1ndgames/GameRadar_GUI")
            print("Server up and listening for connection at " + self.radar.config['server']['ip'] + ":" + self.radar.config['server']['port'] + ' (UDP)')

            # Listen for incoming datagrams
            while True:
                bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
                message = bytesAddressPair[0]
                print(str(message))
                self.unpack_json(message)
                self.radar.received_update = True
