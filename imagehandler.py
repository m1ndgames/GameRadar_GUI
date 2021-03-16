import cv2
from scipy import ndimage
from PIL import Image
import io
import time
import numpy as np


class ImageHandler:
    def __init__(self, radar=None):
        self.radar = radar
        self.radar.imagedata = None

    def run(self):
        while not self.radar.stopthreads:
            if not self.radar.game or not self.radar.map:
                self.radar.mapfile = 'images/noconnection.png'
                map_img = cv2.imread(self.radar.mapfile)
                self.radar.imagedata = self.provide_image_data(map_img)
            else:
                self.radar.mapfile = 'images/games/' + self.radar.game + '/mapimage/' + self.radar.map + '.png'
                map_img = cv2.imread(self.radar.mapfile)

                # Add markers
                marker_img = None
                for o in self.radar.objects:
                    marker_img = self.marker(img=map_img, o=o)

                self.radar.imagedata = self.provide_image_data(marker_img)

                time.sleep(int(self.radar.config['radar']['updatecycle']) / 1000)

    def provide_image_data(self, imgarray):
        """Generate image data using PIL
        """
        img = Image.fromarray(imgarray)

        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img

        return bio.getvalue()

    def marker(self, img, o=None):
        """Place markers on the Map
        """
        # Recolor marker based on playertype
        if o['type'] == 'self':
            color = (0, 255, 0)
            image = 'images/arrow.png'
            scale_percent = 15
        elif o['type'] == 'friend':
            color = (0, 255, 255)
            image = 'images/arrow.png'
            scale_percent = 15
        elif o['type'] == 'extract':
            color = (255, 255, 255)
            image = 'images/extract.png'
            scale_percent = 50
        elif o['type'] == 'target':
            color = (127, 0, 0)
            image = 'images/target.png'
            scale_percent = 25
        elif o['type'] == 'supply':
            color = (255, 255, 255)
            image = 'images/supply.png'
            scale_percent = 15
        elif o['type'] == 'carrier':
            color = (255, 100, 0)
            image = 'images/arrow.png'
            scale_percent = 15
        else:
            color = (255, 0, 0)
            image = 'images/arrow.png'
            scale_percent = 15

        player_marker_plain = Image.open(image)

        im = player_marker_plain.convert('RGBA')
        data = np.array(im)
        red, green, blue, alpha = data.T
        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = color
        im2 = Image.fromarray(data)

        # Rotate the marker according to object rotation
        if 'rotation' in o:
            rotated_player_marker = ndimage.rotate(im2, o['rotation'])
        else:
            # ToDo: Rotate extract based on position to border
            if o['type'] == 'extract':
                rotated_player_marker = ndimage.rotate(im2, 0)
            else:
                rotated_player_marker = ndimage.rotate(im2, 0)

        width = int(rotated_player_marker.shape[1] * scale_percent / 100)
        height = int(rotated_player_marker.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized_player_marker = cv2.resize(rotated_player_marker, dim, interpolation=cv2.INTER_AREA)

        # Regenerate the Map with marker on it
        y1, y2 = o['y'], o['y'] + resized_player_marker.shape[0]
        x1, x2 = o['x'], o['x'] + resized_player_marker.shape[1]

        alpha_s = resized_player_marker[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            img[y1:y2, x1:x2, c] = (alpha_s * resized_player_marker[:, :, c] + alpha_l * img[y1:y2, x1:x2, c])

        return img
