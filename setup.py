#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as fin:
    long_description = fin.read()


setup(
    name='pylint-pytest',
    version='1.1.3',
    author='Reverb Chu',
    author_email='pylint-pytest@reverbc.tw',
    maintainer='Reverb Chu',
    maintainer_email='pylint-pytest@reverbc.tw',
    license='MIT',
    url='https://github.com/reverbc/pylint-pytest',
    description='A Pylint plugin to suppress pytest-related false positives.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests', 'sandbox']),
    install_requires=[
        'pylint',
        'pytest>=4.6',
    ],
    extras_require={
        'pytest_describe': ['pytest_describe'],
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    tests_require=['pytest', 'pytest_describe', 'pylint'],
    keywords=['pylint', 'pytest', 'plugin'],
)
