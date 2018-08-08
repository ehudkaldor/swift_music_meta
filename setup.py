#!/usr/bin/python

from setuptools import setup

setup(name='music_meta',
      version='0.0.1',
      author='ehudkaldor',
      packages=['music_meta'],
      entry_points={
          'paste.filter_factory': [
              'music_meta=music_meta:filter_factory',
          ],
})
