"""Main function of the package and CLI wrapper (entry point)."""


import argparse

import cv2

from imaginator.imaginator import Imaginator
from imaginator.symbol import symbols_line_generator


def create_video(imaginator: Imaginator, name: str = 'default.mp4',
                 frame_rate: float = 24.0,
                 text_line: str = 'HELLO WORLD'
                 ) -> None:

    if not name.endswith('.mp4'):
        name = name + '.mp4'

    text_line = text_line.upper()

    row_cnt = len(imaginator.matrix)
    col_cnt = len(imaginator.matrix[0])

    matrix = [[0] * col_cnt for i in range(row_cnt)]

    frame = imaginator.base_img
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(name, fourcc, frame_rate, (width, height))

    frame = imaginator.make_frame(matrix)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    video.write(frame)

    for line in symbols_line_generator(text_line, reverse=True):
        matrix[1:] = matrix[:-1]
        matrix[0] = line
        frame = imaginator.make_frame(matrix)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        video.write(frame)

    for _ in matrix:
        matrix[1:] = matrix[:-1]
        matrix[0] = [0] * col_cnt
        frame = imaginator.make_frame(matrix)
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
    imgntr = Imaginator()
    return create_video(imaginator=imgntr, name=args.output, text_line=args.string)
