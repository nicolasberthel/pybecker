PyBecker - controlling Becker RF Shutter with Python
====================================================

[![PyPI version](https://img.shields.io/pypi/v/pybecker.svg)](https://pypi.python.org/pypi/pybecker)
[![Requirements Status](https://requires.io/github/nicolasberthel/pybecker/requirements.svg?branch=master)](https://requires.io/github/nicolasberthel/pybecker/requirements/?branch=master)
![Python package](https://github.com/nicolasberthel/pybecker/workflows/Python%20package/badge.svg?branch=master)

This library is based on the work of **ole1986** (https://github.com/ole1986/centronic-py)

PyBecker requires a Becker Centronic USB Stick in order to communicate with the Shutters.
The pairing need as well to be performed before and is not yet part of the library


The goal of this library is to be used in Home assistant custom component to control your becker shutters.
This component is not yet publicly released.

Requirements
------------

From 0.0.5 pybecker uses asyncio it requires pyhton 3.7 or above

Installation
------------

The easiest way to install pybecker library is using [pip](https://pip.pypa.io/en/stable/):
```console
pip install pybecker
```

Usage
-----
The goal of this library is to be used in your home automation component. 
however after installation you can test it by runing
```console
pybecker -a <UP|DOWN|PAIR|HALT> -c <CHANNEL>
```
