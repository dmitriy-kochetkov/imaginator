#!/usr/bin/env python3


import os.path
from setuptools import setup


base_dir = os.path.abspath(os.path.dirname(__file__))


setup(
    name='imaginator',
    author='Dmitriy Kochetkov',
    version='0.0.1',
    description='Package for generating animated text videos',
    long_description=open(os.path.join(base_dir, 'README.md')).read(),
    packages=['imaginator'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'create_video=imaginator.entry:create_video_entry',
        ]
    },
    install_requires=open(os.path.join(base_dir, 'requirements.txt')).readlines(),
    include_package_data=True,
    zip_safe=False,

)
