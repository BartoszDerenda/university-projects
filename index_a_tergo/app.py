import re
import csv
import math
import os
import locale
from clp3 import clp
from collections import defaultdict

locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

alph = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'o', 'p', 'r', 's',
        'ś', 't', 'u', 'ó', 'w', 'x', 'y', 'z', 'ż', 'ź']

def _words_from_line(line):
    "Zwraca listę słów dla linijki tekstu."
    words = re.split('[\W\d]+', line)
    return [w.lower() for w in words if w]


def _sort_stat(stat):
    "Sortuje malejąco listę par według drugiego elementu."
    return sorted(stat, key=lambda p: p[1], reverse=True)

def a_tergo(directory):
    # directory = input("Name of directory with texts: ")
    frequency_list = {}

    for filename in os.scandir(directory):
        if filename.is_file():
            with open(filename.path, 'r') as file:
                text = file.read()
                for line in _words_from_line(text):
                    id = clp.rec(line)
                    if id:
                        word = clp.bform(id[0])
                        if word not in frequency_list:
                            frequency_list[word] = 0
                        frequency_list[word] += 1

    temp = []
    for key, value in frequency_list.items():
        temp.append([key, value])

    # temp = [(k, v) for k, v in result.items()]
    # temp2 = sorted(temp, key=lambda x: x[0][::-1])

    sorted_result = sorted(temp, key=lambda x: locale.strxfrm(x[0][::-1]))


    for item in sorted_result:
       print(item)

a_tergo('grunio')
