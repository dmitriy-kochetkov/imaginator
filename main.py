"""Startup script of the application."""

from imaginator import Imaginator, create_video

if __name__ == '__main__':
    imaginator = Imaginator()
    create_video(imaginator=imaginator, name='hello', frame_rate=24.0, text_line='hello world!')
