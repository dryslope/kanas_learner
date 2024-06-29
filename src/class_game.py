#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import logging
from time import sleep
from constants import FILE_RESULTS, NB_KANAS
from class_conf import Conf
from class_kana_list import KanaList

logging.basicConfig(level=logging.DEBUG)

class Game:
    def __init__(self):
        self.conf = Conf()
        self.kana_list = KanaList()
        self.score = 0
        self.total_time = 0
        self.max_time = 0    
        self.min_time = 1000000

    def prepare(self):
        # Get the list of all kanas from base file
        all_kana_list = KanaList()
        all_kana_list.set_base_list(self.conf.get_kana_type())
        # We get the number of full lists that fit in
        # the number of kanas to guess
        nb_full_lists = self.conf.get_nb_to_guess() // NB_KANAS
        # And get the nb of additional kanas
        nb_additional_kanas = self.conf.get_nb_to_guess() % NB_KANAS
        for _ in range(0, nb_full_lists):
            all_kana_list.shuffle()
            self.kana_list.extend(all_kana_list)
        # Then we add the last kanas after shuffling again
        all_kana_list.shuffle()
        self.kana_list.extend(all_kana_list[:nb_additional_kanas])
        # Finally, shuffle the list to guess
        self.kana_list.shuffle()

    def run_game(self):
        if self.conf.get_lang_to_guess() == 'en':
            self.launch_game_en()
        else:
            self.launch_game_jp
        self.announce_results()
        print()
        self.analyze_records()
        self.save_records()
        print()

    def launch_game_en(self):
        hidden = "EN"
        displayed = "JP"
        for number in range(0, self.conf.get_nb_to_guess()):
            os.system('clear -x')
            print(self.kana_list[number].get_syllable(displayed))
            start = datetime.datetime.now()
            answer = input()
            end = datetime.datetime.now()
            time_round = end - start
            time_raw = time_round.total_seconds()
            self.total_time += time_raw
            if answer != self.kana_list[number].get_syllable(hidden):
                print('Wrong! Answer :', self.kana_list[number].get_syllable(hidden))
                sleep(1.5)
            else:
                self.score += 1
                if time_raw < self.min_time:
                    self.min_time = time_raw
            if time_raw > self.max_time:
                self.max_time = time_raw
        os.system('clear -x')

    def launch_game_jp(self):
        hidden = "JP"
        displayed = "EN"

    def announce_results(self):
        if self.total_time > 60:
            nb_min = int(self.total_time // 60)
            nb_sec = self.total_time % 60
            time_pretty = f'{nb_min} min {nb_sec:.3f}s'
        else:
            time_pretty = f'{self.total_time:.3f}s'
        print()
        print(f"The end! Score: {self.score}/{self.conf.get_nb_to_guess()}, duration: {time_pretty}.")

    def save_records(self):
        if os.path.exists(FILE_RESULTS):
            open_mode = 'a'  # append if file already exists
        else:
            open_mode = 'w' # else create file
        with open(FILE_RESULTS, open_mode) as filestream:
            line_data = f'{self.score}  {self.conf.get_nb_to_guess()}  {self.total_time}  {self.min_time}  {self.max_time}'
            filestream.write(line_data)
            filestream.write('\n')

    def analyze_records(self):
        try:
            with open(FILE_RESULTS, 'r+') as filestream:
                content = filestream.read()
        except FileNotFoundError:
            content = ""
        index_min = 3
        index_max = 4
        best_min = 100000.
        best_max = 0.
        for data in content.splitlines():
            list_data = data.split("  ")
            if float(list_data[index_min]) < best_min:
                best_min = float(list_data[index_min])
            if float(list_data[index_max]) > best_max:
                best_max = float(list_data[index_max])
        if content == "":
            previous_min = None 
            previous_max = None
        else:
            previous_min = f"{best_min:.3f}s"
            previous_max = f"{best_max:.3f}s"
        if self.min_time < best_min:
            print(f"Woow that was so fast! New fastest time to answer: {self.min_time:.3f}s (previous: {previous_min}).")
        if self.max_time > best_max:
            print(f"You have to be faster! New longest time to answer: {self.max_time:.3f}s (previous: {previous_max}).")