import cv2
import os
import json


class Imaginator:

    def __init__(self, config_file='config.txt', base_img_name='background.png', overlay_img_name='overlay.png'):
        self.config = config_file
        self.base_img_path = 'img' + os.sep + base_img_name
        self.over_img_path = 'img' + os.sep + overlay_img_name
        self.target = 'output'
        self.matrix = []
        self.base_img = None
        self.over_img = None

    def load(self):
        if not self.load_config():
            return

        if not self.load_images():
            return

    def load_images(self):
        return self.load_base_img() and self.load_over_img()

    def load_base_img(self):
        try:
            self.base_img = cv2.imread(self.base_img_path, cv2.IMREAD_COLOR)
        except Exception as e:
            print('Base image loading failed\n', e)
            return False
        return True

    def load_over_img(self):
        try:
            self.over_img = cv2.imread(self.over_img_path, cv2.IMREAD_COLOR)
        except Exception as e:
            print('Overlay image loading failed\n', e)
            return False
        return True

    def load_config(self):
        try:
            with open(self.config) as conf:
                json_str = conf.read()
                self.matrix = json.loads(json_str)
        except Exception as e:
            print('Config loading failed\n', e)
            return False

        return True

    def print_matrix(self):
        for row in self.matrix:
            for cell in row:
                print('({:4}:{:4})({:4}:{:4});'.format(cell['x0'], cell['y0'], cell['x1'], cell['y1']), end=' ')
            print('\n', end='')

    def make_mixed_image(self, msk_list, name='temp.png'):
        mixed_image = self.base_img.copy()

        for matrix_i, matrix_j in msk_list:
            bounds = self.matrix[matrix_i][matrix_j]
            mixed_image[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']] = self.over_img[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']]

        name = self.target + os.sep + name
        cv2.imwrite(name, mixed_image)
        print('{} saved'.format(name))

    def make_mixed_frame(self, msk_list):
        mixed_frame = self.base_img.copy()

        for matrix_i, matrix_j in msk_list:
            bounds = self.matrix[matrix_i][matrix_j]
            mixed_frame[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']] = self.over_img[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']]

        return mixed_frame
