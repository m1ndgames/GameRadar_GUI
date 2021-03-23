import socket
import json
import time
import random


class RadarClient:
    def __init__(self):
        self.game = None
        self.map = None
        self.mapsize = None
        self.player_position = None
        self.friend_position = None
        self.enemy_1_position = None
        self.enemy_2_position = None
        self.extract_position = None
        self.target_position = None
        self.supply_position = None

    def pack_json(self):
        data = {
            'game': self.game,
            'map': self.map,
            'map_size': self.mapsize,
            'objects': [
                {
                    'type': 'self',
                    'x': self.player_position['x'],
                    'y': self.player_position['y'],
                    'rotation': self.player_position['rotation'],
                },
                {
                    'type': 'friend',
                    'x': self.friend_position['x'],
                    'y': self.friend_position['y'],
                    'rotation': self.friend_position['rotation'],
                },
                {
                    'type': 'enemy',
                    'x': self.enemy_1_position['x'],
                    'y': self.enemy_1_position['y'],
                    'rotation': self.enemy_1_position['rotation'],
                },
                {
                    'type': 'enemy',
                    'x': self.enemy_2_position['x'],
                    'y': self.enemy_2_position['y'],
                    'rotation': self.enemy_2_position['rotation'],
                    'carrier': True
                },
                {
                    'type': 'extract',
                    'x': 0,
                    'y': int(self.mapsize[1] / 2),
                },
                {
                    'type': 'extract',
                    'x': self.mapsize[0],
                    'y': int(self.mapsize[1] / 2),
                },
                {
                    'type': 'extract',
                    'x': int(self.mapsize[0] / 2),
                    'y': 0,
                },
                {
                    'type': 'extract',
                    'x': int(self.mapsize[0] / 2),
                    'y': self.mapsize[1],
                },
                {
                    'type': 'target',
                    'x': self.target_position['x'],
                    'y': self.target_position['y'],
                },
                {
                    'type': 'supply',
                    'x': self.supply_position['x'],
                    'y': self.supply_position['y'],
                }
            ]
        }

        json_data_string = json.dumps(data)
        return json_data_string

    def run(self):
        # Specify the game
        self.game = 'huntshowdown'

        # Map name
        self.map = 'Bayou'

        # The maps size
        self.mapsize = (3000, 3000)

        # Place some random markers on the map
        while True:
            self.player_position = {'x': random.randrange(self.mapsize[0]), 'y': random.randrange(self.mapsize[1]), 'rotation': random.randrange(360)}
            self.friend_position = {'x': random.randrange(self.mapsize[0]), 'y': random.randrange(self.mapsize[1]), 'rotation': random.randrange(360)}
            self.enemy_1_position = {'x': random.randrange(self.mapsize[0]), 'y': random.randrange(self.mapsize[1]), 'rotation': random.randrange(360)}
            self.enemy_2_position = {'x': random.randrange(self.mapsize[0]), 'y': random.randrange(self.mapsize[1]), 'rotation': random.randrange(360)}
            self.target_position = {'x': random.randrange(self.mapsize[0]), 'y': random.randrange(self.mapsize[1])}
            self.supply_position = {'x': random.randrange(self.mapsize[0]), 'y': random.randrange(self.mapsize[1])}

            databytes = str.encode(self.pack_json())
            server = ("127.0.0.1", 1337)

            # Create a UDP socket at client side
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            # Send to server using created UDP socket
            UDPClientSocket.sendto(databytes, server)

            time.sleep(0.25)


if __name__ == '__main__':
    radar = RadarClient()
    radar.run()
