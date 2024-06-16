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

    def start(self):
        score = 0
        total_time = 0
        max_time = 0    
        min_time = 1000000

        if self.conf.get_lang_to_guess() == 'en':
            hidden = "EN"
            displayed = "JP"
        else:
            hidden = "JP"
            displayed = "EN"
        for number in range(0, self.conf.get_nb_to_guess()):
            os.system('clear -x')
            print(self.kana_list[number].get_syllable(displayed))
            start = datetime.datetime.now()
            answer = input()
            end = datetime.datetime.now()
            time_round = end - start
            time_raw = time_round.total_seconds()
            total_time += time_raw
            if answer != self.kana_list[number].get_syllable(hidden):
                print('Wrong! Answer :', self.kana_list[number].get_syllable(hidden))
                sleep(1.5)
            else:
                score += 1
                if time_raw < min_time:
                    min_time = time_raw
            if time_raw > max_time:
                max_time = time_raw
        os.system('clear -x')
        if total_time > 60:
            nb_min = int(total_time // 60)
            nb_sec = total_time % 60
            time_pretty = f'{nb_min} min {nb_sec:.3f} sec'
        else:
            time_pretty = f'{total_time:.3f} sec'
        line_data = f'{score}  {self.conf.get_nb_to_guess()}  {total_time}  {min_time}  {max_time}'
        print(f"The end ! Score: {score}/{self.conf.get_nb_to_guess()}, duration: {time_pretty}")
        print()
        self.analyze_records(line_data)
        self.save_records(line_data)
        print()

    @staticmethod
    def save_records(line_data):
        if os.path.exists(FILE_RESULTS):
            open_mode = 'a'  # append if file already exists
        else:
            open_mode = 'w' # else create file
        with open(FILE_RESULTS, open_mode) as filestream:
            filestream.write(line_data)
            filestream.write('\n')

    @staticmethod
    def analyze_records(line_data):
        try:
            with open(FILE_RESULTS, 'r+') as filestream:
                content = filestream.read()
        except FileNotFoundError:
            content = ""
        index_score = 0
        index_number = 1
        index_min = 3
        index_max = 4
        list_my_data = line_data.split('  ')
        best_mean = 0
        best_min = 100000.
        best_max = 0.
        for data in content.splitlines():
            list_data = data.split("  ")
            mean_score = int(list_data[index_score]) / int(list_data[index_number])
            if mean_score > best_mean:
                best_mean = mean_score
            if float(list_data[index_min]) < best_min:
                best_min = float(list_data[index_min])
            if float(list_data[index_max]) > best_max:
                best_max = float(list_data[index_max])
        my_mean = int(list_my_data[index_score]) / int(list_my_data[index_number])
        if my_mean == 1.0:
            print(f"Perfect score, congratulations !")
        elif my_mean > best_mean:
            print(f"Congratulations! You beat the best score of {best_mean} with this new one: {my_mean}.")
        else:
            print(f"Great, but not as good as the time you did {best_mean}, this time: {my_mean}.")
        my_min = float(list_my_data[index_min])
        if my_min < best_min:
            print(f"Wow that was fast! You beat your previous faster answer of {best_min} with this new min: {my_min}.")
        my_max = float(list_my_data[index_max])
        if my_max > best_max:
            print(f"You gotta be faster! Your longest time to answer is now {my_max} instead of your previous {best_max}.")
            
