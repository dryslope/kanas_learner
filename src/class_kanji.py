#!/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from constants import (SEPARATOR, INDEX_EN, INDEX_JP, INDEX_OGEN)

class Kanji():
    def __init__(self, line):
        """
        Create kanji from one line of a kana file.
        OG is the pronounciation of the kanji, 
        """
        self.__dict_syllable = {
            "JP": line.split(SEPARATOR)[INDEX_JP],
            "EN": line.split(SEPARATOR)[INDEX_EN],
            "OGEN": line.split(SEPARATOR)[INDEX_OGEN],
        }

    def get_word(self, type):
        return self.__dict_words[type]