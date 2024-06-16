#!/bin/env python3
# -*- coding: utf-8 -*-

import random
from class_kana import Kana
from constants import ALL_KANAS_DIR

class KanaList(list):
    def __init__(self):
        pass

    def set_base_list(self, kana_type):
        filepath = f"{ALL_KANAS_DIR}/{kana_type}"
        with open(filepath, 'r') as filestream:
            file_content = filestream.read()
        for line in file_content.splitlines():
            self.append(Kana(line))

    def shuffle(self):
        random.seed()  # initialize the random number generator
        length = len(self) 
        for index in range(length):
            jndex = random.randint(0, length-1)
            # swap the elements in list at positions index and jndex
            self[index], self[jndex] = self[jndex], self[index] 

