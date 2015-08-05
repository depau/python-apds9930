#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r") as f:
        return f.read()

setup(
    name = "python-apds9930",
    version = "0.1",
    author = "Davide Depau",
    author_email = "apps@davideddu.org",
    description = ("Python bindings for the Avago APDS-9930 I2C Ambient Light and proximity sensor."),
    license = "GPLv2",
    keywords = "i2c bindings sensor hardware linux raspberry raspberrypi",
    url = "http://davideddu.org/blog/apds-9930-python-module",
    packages=['apds9930'],
    long_description=read('README.md'),
    requires=["smbus"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
