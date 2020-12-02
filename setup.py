#!/usr/bin/env python3


import codecs
import os.path
import re
from setuptools import setup


base_dir = os.path.abspath(os.path.dirname(__file__))


with codecs.open(os.path.join(base_dir, 'imaginator', '__init__.py')) as stream:
    data = stream.read()
    version = re.search(r'__version__\s*=\s*\'(.+)\'', data).group(1)
    author = re.search(r'__author__\s*=\s*\'(.+)\'', data).group(1)


setup(
    name='imaginator',
    author=author,
    version=version,
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
