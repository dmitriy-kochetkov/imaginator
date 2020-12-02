"""Main function of the package and CLI wrapper (entry point)."""


import argparse

import cv2

from imaginator.imaginator import Imaginator
from imaginator.symbol import symbols_line_generator


def create_video(name: str = 'default.mp4', frame_rate: float = 24.0, text_line: str = 'HELLO WORLD') -> None:

    if not name.endswith('.mp4'):
        name = name + '.mp4'

    text_line = text_line.upper()

    imgntr = Imaginator(base_img_name='background_full.png', overlay_img_name='overlay_full.png')

    matrix = []
    for row in range(24):
        matrix.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    frame = imgntr.base_img
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(name, fourcc, frame_rate, (width, height))

    frame = imgntr.make_frame(matrix)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    video.write(frame)

    for line in symbols_line_generator(text_line, reverse=True):
        matrix[1:] = matrix[:-1]
        matrix[0] = line
        frame = imgntr.make_frame(matrix)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        video.write(frame)

    for _ in matrix:
        matrix[1:] = matrix[:-1]
        matrix[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        frame = imgntr.make_frame(matrix)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()
    print('{} saved'.format(name))


def create_video_entry() -> None:
    """Parse command line arguments and call `create_video` function with them."""
    parser = argparse.ArgumentParser()
    parser.add_argument('string', help='Input string')
    parser.add_argument('-o', '--output', default='result.mp4', help='Path to result file')
    args = parser.parse_args()
    return create_video(name=args.output, text_line=args.string)
