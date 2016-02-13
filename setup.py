#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='androidvideo',
    packages=['androidvideo'],
    version='1.0.0',
    description=('Create Android compatible videos that play in ANY Android '
                 'device without third party software.'),
    author='Carlo Eduardo Rodriguez Espino',
    author_email='carloeduardorodriguez@gmail.com',
    url='https://github.com/CarloRodriguez/androidvideo',
    download_url=('https://github.com/CarloRodriguez/androidvideo/archive/'
                  'master.zip'),
    keywords='android video videos compatible play',
    license='GPL',
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            'androidvideo = androidvideo.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
    ],
)
