#!/usr/bin/env python3

import glob
import os

from setuptools import setup

from speech import __version__

I18N_FILES = []
for file_path in glob.glob('locale/*/LC_MESSAGES/*.mo'):
    lang = file_path[len('locale/'):]
    target_path = os.path.dirname(os.path.join('share/locale', lang))
    print(target_path)
    I18N_FILES.append((target_path, [file_path]))

DICT_FILES = []
for file_path in glob.glob('dict/*/*'):
    lang = file_path[len('dict/'):]
    target_path = os.path.dirname(os.path.join(
        'share/gspeech/dict',
        lang
    ))
    DICT_FILES.append((target_path, [file_path]))

ICONS_FILES = []
for file_path in glob.glob('icons/*'):
    ICONS_FILES.append((
        'share/icons/hicolor/scalable/apps',
        [file_path]
    ))

setup(
    name='gspeech',
    version=__version__,
    description=("""
        A minimal GUI for the Text To Speech 'Svox Pico'.
        Read clipboard or selected text in different languages
        and manage it : pause, stop, replay.";
    """),
    author='mothsart',
    author_email='jerem.ferry@gmail.com',
    url='https://github.com/mothsart/gSpeech',
    packages=[
        'speech',
        'speech.widgets',
        'speech.workers', 'speech.workers.fr_FR'
    ],
    package_data={'speech': ['gspeech.conf']},
    data_files=I18N_FILES + DICT_FILES + ICONS_FILES,
    entry_points={
        'console_scripts': [
            'gspeech = speech.main:main',
            'gspeech-cli = speech.cli:main'
        ]
    }
)
