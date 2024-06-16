#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import random
import datetime
from time import sleep
from constants import (SEPARATOR, INDEX_EN, INDEX_JP)

class Kana():
    def __init__(self, line):
        """
        Create kana from one line of a kana file.
        """
        self.__dict_syllable = {
            "JP": line.split(SEPARATOR)[INDEX_JP],
            "EN": line.split(SEPARATOR)[INDEX_EN],
        }

    def get_syllable(self, type):
        return self.__dict_syllable[type]