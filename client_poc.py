import socket
import json
import time
import random


class RadarClient:
    def __init__(self):
        self.player_position = None
        self.friend_position = None
        self.enemy_1_position = None
        self.enemy_2_position = None
        self.extract_position = None
        self.target_position = None
        self.supply_position = None
        self.game = 'huntshowdown'
        self.map = 'Bayou'

    def pack_json(self):
        data = {
            'game': self.game,
            'map': self.map,
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
                    'x': self.extract_position['x'],
                    'y': self.extract_position['y'],
                },
                {
                    'type': 'target',
                    'x': self.target_position['x'],
                    'y': self.target_position['y'],
                },
                {
                    'type': 'supply',
                    'x': self.target_position['x'],
                    'y': self.target_position['y'],
                }
            ]
        }

        json_data_string = json.dumps(data)
        return json_data_string

    def run(self):
        while True:
            self.player_position = {'x': random.randrange(100), 'y': random.randrange(100), 'rotation': random.randrange(360)}
            self.friend_position = {'x': random.randrange(100), 'y': random.randrange(100), 'rotation': random.randrange(360)}
            self.enemy_1_position = {'x': random.randrange(100), 'y': random.randrange(100), 'rotation': random.randrange(360)}
            self.enemy_2_position = {'x': random.randrange(100), 'y': random.randrange(100), 'rotation': random.randrange(360)}
            self.extract_position = {'x': random.randrange(100), 'y': random.randrange(100), 'rotation': random.randrange(360)}
            self.target_position = {'x': random.randrange(100), 'y': random.randrange(100), 'rotation': random.randrange(360)}
            self.supply_position = {'x': random.randrange(100), 'y': random.randrange(100), 'rotation': random.randrange(360)}

            bytesToSend         = str.encode(self.pack_json())
            serverAddressPort   = ("127.0.0.1", 1337)
            bufferSize          = 1024

            # Create a UDP socket at client side
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            # Send to server using created UDP socket
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            time.sleep(0.01)

if __name__ == '__main__':
    radar = RadarClient()
    radar.run()
