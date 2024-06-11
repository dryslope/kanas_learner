#!/bin/env python3
# -*- coding: utf-8 -*-


import os
import argparse
import random
import datetime
from time import sleep

NB_KANAS = 46
HOME = os.environ["HOME"]
LEARNER_DIR = os.environ.get("LEARNER", f"{HOME}/kanas_learner")
FILE_DATA = f"{LEARNER_DIR}/records.metrics"


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


def get_kanas(kana_type):
    filepath = f"{LEARNER_DIR}/{kana_type}"
    with open(filepath, 'r') as filestream:
        content = filestream.read()
    list_kanas = content.splitlines()
    return list_kanas


def prepare_list(nb_to_guess, list_kanas):
    pass
    # We get the number of full lists that fit in
    # the number of kanas to guess
    nb_full_lists = nb_to_guess // NB_KANAS
    # And get the nb of additional kanas
    nb_additional_kanas = nb_to_guess % NB_KANAS 

    final_list = []

    for _ in range(0, nb_full_lists):
        shuffle_list(list_kanas)
        final_list.extend(list_kanas)
    shuffle_list(list_kanas)
    final_list.extend(list_kanas[:nb_additional_kanas])
    return final_list


def shuffle_list(list_kanas):
    random.seed() # initialize the random number generator
    n = len(list_kanas) 
    for i in range(n):
        j = random.randint(0, n-1)
        # swap the elements in lst at positions i and j
        list_kanas[i], list_kanas[j] = list_kanas[j], list_kanas[i]


def launch_game(args, list_kanas):
    score = 0
    total_time = 0
    max_time = 0    
    min_time = 1000000
    if args.guess == 'fr':
        hidden = 1
        displayed = 0
    else:
        hidden = 0
        displayed = 1
    # Get the number of kanas to guee
    # Either the nb in cmdline or all the kanas
    if args.number:
        nb_to_iterate = args.number
    else:
        nb_to_iterate = len(list_kanas)

    shuffled_full_list = prepare_list(nb_to_iterate, list_kanas)

    for number in range(0, nb_to_iterate):
        os.system('clear -x')
        print(shuffled_full_list[number].split(':')[displayed])
        start = datetime.datetime.now()
        answer = input()
        end = datetime.datetime.now()
        time_round = end - start
        time_raw = time_round.total_seconds()
        total_time += time_raw
        if answer != shuffled_full_list[number].split(':')[hidden]:
            print('Wrong! Answer :', shuffled_full_list[number].split(':')[hidden])
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
    line_data = f'{score}  {args.number}  {total_time}  {min_time}  {max_time}'
    print(f"The end ! Score: {score}/{args.number}, duration: {time_pretty}")
    print()
    analyze_records(line_data)
    save_records(line_data)


def save_records(line_data):
    with open(FILE_DATA, 'w+') as filestream:
        filestream.write(line_data)
        filestream.write('\n')


def analyze_records(line_data):
    try:
        with open(FILE_DATA, 'r+') as filestream:
            content = filestream.read()
    except FileNotFoundError:
        content = ""
    index_score = 0
    index_number = 1
    index_total = 2
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
        

def main():
    args = parse_args()
    list_kanas = get_kanas(args.kana_type)
    launch_game(args, list_kanas)


if __name__ == "__main__":
    main()
