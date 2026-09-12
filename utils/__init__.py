#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/12 22:00
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   __init__.py.py
# @Desc     :   

"""
****************************************************************
Utility Module - Comprehensive Toolkit
----------------------------------------------------------------
This module provides a comprehensive suite of utility functions
and classes designed for general data processing tasks.
****************************************************************
"""

__author__ = "Shawn Yu"
__version__ = "0.1.0"

from .decorator import (beautifier,
                        timer, clock, countdown)
from .helper import (Beautifier, Timer,
                     RandomSeed)
from .highlighter import (black, red, green, yellow, blue, purple, cyan, white,
                          bold, underline, invert, strikethrough,
                          stars, lines, sharps)

__all__ = [
    "beautifier",
    "timer", "clock",
    "countdown",

    "Beautifier",
    "Timer",
    "RandomSeed",

    "black", "red", "green", "yellow", "blue", "purple", "cyan", "white",
    "bold", "underline", "invert", "strikethrough",
    "stars", "lines", "sharps",
]
