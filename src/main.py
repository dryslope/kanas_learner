#!/bin/env python3
# -*- coding: utf-8 -*-

import os

from class_game import Game

def main():
    try:
        the_game = Game()
        the_game.prepare()
        the_game.run_game()
    except KeyboardInterrupt:
        os.system('clear -x')
        print("Game was manually stopped, bye!")

if __name__ == "__main__":
    main()
