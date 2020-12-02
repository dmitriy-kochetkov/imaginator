"""Startup script of the application."""


from imaginator import create_video

if __name__ == '__main__':
    create_video(name='hello', frame_rate=24.0, text_line='hello world!')
