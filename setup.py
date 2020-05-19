#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='pylint-pytest',
    version='0.1',
    author='Reverb Chu',
    author_email='pylint-pytest@reverbc.tw',
    maintainer='Reverb Chu',
    maintainer_email='pylint-pytest@reverbc.tw',
    license='MIT',
    url='https://github.com/reverbc/pylint-pytest',
    description='A Pylint plugin to suppress pytest fixture related false positive warnings.',
    py_modules=['pylint_pytest'],
    install_requires=[
        'pylint',
        'pytest>=4.6',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    tests_require=['pytest', 'pylint'],
    keywords=['pylint', 'pytest', 'plugin'],
)
