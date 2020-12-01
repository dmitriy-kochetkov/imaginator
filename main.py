import cv2

from imaginator import Imaginator
from symbol import reversed_symbols_line_generator


def create_video(name='default.mp4', frame_rate=24.0, text_line='HELLO WORLD'):

    if not name.endswith('.mp4'):
        name = name + '.mp4'

    text_line = text_line.upper()

    imgntr = Imaginator(base_img_name='background_black.png')
    imgntr.load()

    matrix = []
    for row in range(24):
        matrix.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    frame = imgntr.base_img
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(name, fourcc, frame_rate, (width, height))

    frame = make_frame(imgntr, matrix)
    video.write(frame)

    for line in reversed_symbols_line_generator(text_line):
        matrix[1:] = matrix[:-1]
        matrix[0] = line
        frame = make_frame(imgntr, matrix)
        video.write(frame)

    for i in range(len(matrix)):
        matrix[1:] = matrix[:-1]
        matrix[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        frame = make_frame(imgntr, matrix)
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()
    print('{} saved'.format(name))


def make_frame(imgntr, matrix):
    msk_list = convert_matrix_to_mask_list(matrix)
    return imgntr.make_mixed_frame(msk_list=msk_list)


def convert_matrix_to_mask_list(matrix):
    result = []
    for row in range(len(matrix)):
        for cell in range(len(matrix[row])):
            if matrix[row][cell]:
                result.append((row, cell))
    return result


if __name__ == '__main__':
    create_video(name='hello', frame_rate=15.0, text_line='hello world!')
