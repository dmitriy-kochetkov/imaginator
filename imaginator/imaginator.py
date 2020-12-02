import os
from typing import Any, List, Tuple
import json

import cv2
import numpy


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
IMG_PATH = os.path.join(BASE_PATH, 'img')
DEFAULT_CONFIG_PATH = os.path.join(BASE_PATH, 'config.txt')


class Imaginator:
    def __init__(
            self, config_file: str = DEFAULT_CONFIG_PATH, base_img_name: str = 'background.png',
            overlay_img_name: str = 'overlay.png'
    ) -> None:
        """
        :param config_file: path to config file with coordinates (json)
        :param base_img_name: path to base image
        :param overlay_img_name: path to overlay image
        """
        self.config = config_file
        self.base_img_path = os.path.join(IMG_PATH, base_img_name)
        self.over_img_path = os.path.join(IMG_PATH, overlay_img_name)
        self.target = 'output'
        self.matrix = load_json_config(self.config)
        self.base_img = load_image(self.base_img_path)
        self.over_img = load_image(self.over_img_path)

    def print_matrix(self) -> None:
        for row in self.matrix:
            for cell in row:
                print('({:4}:{:4})({:4}:{:4});'.format(cell['x0'], cell['y0'], cell['x1'], cell['y1']), end=' ')
            print()

    def make_mixed_image(self, msk_list, name: str = 'temp.png') -> None:
        mixed_image = self.base_img.copy()

        for matrix_i, matrix_j in msk_list:
            bounds = self.matrix[matrix_i][matrix_j]
            mixed_image[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']] = self.over_img[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']]

        name = self.target + os.sep + name
        cv2.imwrite(name, mixed_image)
        print('{} saved'.format(name))

    def make_mixed_frame(self, msk_list: List[Tuple[int, int]]) -> numpy.ndarray:
        mixed_frame = self.base_img.copy()

        for matrix_i, matrix_j in msk_list:
            bounds = self.matrix[matrix_i][matrix_j]
            mixed_frame[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']] = self.over_img[bounds['y0']:bounds['y1'], bounds['x0']:bounds['x1']]

        return mixed_frame

    def make_frame(self, matrix: List[List[int]]) -> numpy.ndarray:
        msk_list = convert_matrix_to_mask_list(matrix)
        return self.make_mixed_frame(msk_list=msk_list)


def convert_matrix_to_mask_list(matrix: List[List[int]]) -> List[Tuple[int, int]]:
    result = []

    for row in range(len(matrix)):
        for cell in range(len(matrix[row])):
            if matrix[row][cell]:
                result.append((row, cell))
    return result


def load_image(path: str) -> numpy.ndarray:
    """Load and return specified image via cv2 library."""
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError('wrong image format or file does not exist: {}'.format(path))
    return cv2.imread(path, cv2.IMREAD_COLOR)


def load_json_config(path: str) -> Any:
    """Load and return specified json config."""
    with open(path, encoding='utf-8') as conf:
        json_str = conf.read()
        return json.loads(json_str)
