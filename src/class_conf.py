#!/bin/env python3
# -*- coding: utf-8 -*-

import argparse

class Conf():
    
    def __init__(self):
        args = self.parse_args()
        self.__kana_type = args.kana_type
        self.__lang_to_guess = args.guess
        self.__nb_to_guess = args.number

    def get_kana_type(self):
        return self.__kana_type
    
    def get_lang_to_guess(self):
        return self.__lang_to_guess
    
    def get_nb_to_guess(self):
        return self.__nb_to_guess
    
    def __str__(self):
        res = f"kana_type: {self.__kana_type}\
        lang_to_guess: {self.__lang_to_guess}\
        nb_to_guess: {self.__nb_to_guess}"
        return res

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
                '-k', '--kanas',
                dest="kana_type",
                choices=["katakana", "hiragana"],
                help="Which kind of kana you want to learn."
        )
        parser.add_argument(
                '-g',
                '--guess',
                dest="guess",
                choices=["en", "jp"],
                help="Which language you'll write to guess."
        )
        parser.add_argument(
                '-n',
                '--number',
                dest="number",
                type=int,
                help="Number of kanas to guess (26 different)."
        )
        args = parser.parse_args()
        return args
    
