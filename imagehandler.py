import copy

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
        self.current_map = None
        self.map_img = None

    def update_map_image(self):
        self.current_map = self.radar.map
        self.radar.mapfile = 'images/games/' + self.radar.game + '/mapimage/' + self.radar.map + '.png'
        original_map = cv2.imread(self.radar.mapfile)
        self.map_img = cv2.resize(original_map, (self.radar.map_size[0], self.radar.map_size[1]), interpolation=cv2.INTER_CUBIC)

    def remove_percentage(self, percentage, value):
        percentage_of = value * (percentage / 100)
        return int(value - percentage_of)

    def add_percentage(self, percentage, value):
        percentage_of = value * (percentage / 100)
        return int(value + percentage_of)

    def crop_image(self, img):
        width = int(img.shape[0])
        height = int(img.shape[1])

        # Zoom map based on zoom level
        crop_percentage = 100 - self.radar.zoom_level

        new_width = self.remove_percentage(crop_percentage, int(img.shape[1]))
        new_height = self.remove_percentage(crop_percentage, int(img.shape[0]))

        cropsize_remove_width = width - new_width
        cropsize_remove_height = height - new_height  # ToDO: needed?!

        cropsize = cropsize_remove_width

        if cropsize_remove_width > 0:
            bbox = None
            for o in self.radar.objects:
                if o['type'] == 'self':
                    bbox = [o['x'] - cropsize, o['y'] - cropsize, o['x'] + cropsize, o['y'] + cropsize]

            x1, y1, x2, y2 = bbox
            if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
                img, x1, x2, y1, y2 = self.pad_img_to_fit_bbox(img, x1, x2, y1, y2)
            return img[y1:y2, x1:x2, :]
        else:
            return img

    def pad_img_to_fit_bbox(self, img, x1, x2, y1, y2):
        img = cv2.copyMakeBorder(img, - min(0, y1), max(y2 - img.shape[0], 0), -min(0, x1), max(x2 - img.shape[1], 0), cv2.BORDER_CONSTANT)

        y2 += -min(0, y1)
        y1 += -min(0, y1)
        x2 += -min(0, x1)
        x1 += -min(0, x1)
        return img, x1, x2, y1, y2

    def run(self):
        while not self.radar.stopthreads:
            if not self.radar.game or not self.radar.map:
                self.radar.mapfile = 'images/noconnection.png'
                map_img = cv2.imread(self.radar.mapfile)
                self.radar.imagedata = self.provide_image_data(map_img)
            else:
                if self.radar.received_update:
                    if self.current_map != self.radar.map or not self.current_map:
                        self.update_map_image()

                    # Create a copy of the map data
                    map_img = copy.deepcopy(self.map_img)

                    # Add markers
                    map_img_with_markers = self.place_markers(img=map_img)

                    # Crop image
                    if self.radar.zoom_level >= 90:
                        self.radar.zoom_level = 90
                    elif self.radar.zoom_level <= 0:
                        self.radar.zoom_level = 0

                    cropped_image = self.crop_image(map_img_with_markers)

                    # Make sure we use the full gui
                    final_image = cv2.resize(cropped_image, (800, 800), interpolation=cv2.INTER_CUBIC)

                    # save the final image for the gui
                    self.radar.imagedata = self.provide_image_data(final_image)

                self.radar.received_update = False

    def provide_image_data(self, imgarray):
        """Generate image data using PIL
        """
        img = Image.fromarray(imgarray)

        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img

        return bio.getvalue()

    def place_markers(self, img):
        """Place markers on the Map
        """
        # Add markers
        marker_img = None
        original_map_size = self.map_img.shape
        scale_percent = (abs(100 - original_map_size[0]) / original_map_size[0]) * 100
        #print(str(scale_percent))
        #if self.radar.zoom_level > 100:
        #    scale_percent = scale_percent - 10

        for o in self.radar.objects:
            # Recolor marker based on playertype
            if o['type'] == 'self':
                color = (0, 255, 0)
                image = 'images/arrow.png'
            elif o['type'] == 'friend':
                color = (0, 255, 255)
                image = 'images/arrow.png'
            elif o['type'] == 'extract':
                color = (255, 255, 255)
                image = 'images/extract.png'
            elif o['type'] == 'target':
                color = (127, 0, 0)
                image = 'images/target.png'
            elif o['type'] == 'supply':
                color = (255, 255, 255)
                image = 'images/supply.png'
            elif o['type'] == 'carrier':
                color = (255, 100, 0)
                image = 'images/arrow.png'
            else:
                color = (255, 0, 0)
                image = 'images/arrow.png'

            # Open marker image
            player_marker_plain = Image.open(image)
            player_marker_plain = player_marker_plain.convert('RGBA')

            # change its color
            data = np.array(player_marker_plain)
            red, green, blue, alpha = data.T
            white_areas = (red == 255) & (blue == 255) & (green == 255)
            data[..., :-1][white_areas.T] = color
            colored_marker = Image.fromarray(data)

            # Rotate the marker according to object rotation
            if 'rotation' in o:
                rotated_player_marker = ndimage.rotate(colored_marker, o['rotation'])
            else:
                # ToDo: Rotate extract based on position to border
                if o['type'] == 'extract':
                    rotated_player_marker = ndimage.rotate(colored_marker, self.distance_to_border(o['x'], o['y']))
                else:
                    rotated_player_marker = ndimage.rotate(colored_marker, 0)

            width = int(rotated_player_marker.shape[1] * scale_percent / 100)
            height = int(rotated_player_marker.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized_player_marker = cv2.resize(rotated_player_marker, dim, interpolation=cv2.INTER_AREA)

            img = self.merge_image(img, resized_player_marker, o['x'], o['y'])

        return img

    def distance_to_border(self, pos_x, pos_y):
        map_dimensions = self.map_img.shape
        height = map_dimensions[0]
        width = map_dimensions[1]

        x_distance_left = 0 + pos_x
        x_distance_right = height - pos_x
        y_distance_bottom = 0 + pos_y
        y_distance_top = width - pos_y

        distances = {
            'left': x_distance_left,
            'right': x_distance_right,
            'bottom': y_distance_bottom,
            'top': y_distance_top
        }

        sorted_by_distance = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
        nearest_border = next(iter(sorted_by_distance))
        if nearest_border == 'left':
            rotation = 90
        elif nearest_border == 'right':
            rotation = 270
        elif nearest_border == 'bottom':
            rotation = 0
        else:
            rotation = 180

        return rotation

    def merge_image(self, back, front, x, y):
        # convert to rgba
        if back.shape[2] == 3:
            back = cv2.cvtColor(back, cv2.COLOR_BGR2BGRA)
        if front.shape[2] == 3:
            front = cv2.cvtColor(front, cv2.COLOR_BGR2BGRA)

        # crop the overlay from both images
        bh, bw = back.shape[:2]
        fh, fw = front.shape[:2]
        x1, x2 = max(x, 0), min(x + fw, bw)
        y1, y2 = max(y, 0), min(y + fh, bh)
        front_cropped = front[y1 - y:y2 - y, x1 - x:x2 - x]
        back_cropped = back[y1:y2, x1:x2]

        alpha_front = front_cropped[:, :, 3:4] / 255
        alpha_back = back_cropped[:, :, 3:4] / 255

        # replace an area in result with overlay
        result = back.copy()
        result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:, :, :3] + (1 - alpha_front) * back_cropped[:, :, :3]
        result[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front * alpha_back) * 255

        return result
