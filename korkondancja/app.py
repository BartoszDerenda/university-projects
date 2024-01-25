import re
import os
from clp3 import clp
'''
import csv
import math
import locale
import nltk
from nltk import tokenize
from collections import defaultdict
'''

# locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")
# nltk.download('punkt')

def _words_from_line(line):
    "Zwraca listę słów dla linijki tekstu."
    words = re.split('[\W\d]+', line)
    return [w.lower() for w in words if w]

def _sort_stat(stat):
    "Sortuje malejąco listę par według drugiego elementu."
    return sorted(stat, key=lambda p: p[1], reverse=True)

def korkondancja():
    word_input = input('Wprowadź wyszukiwane słowo (np. świnka)\n> ')

    words = clp.forms_all(word_input)

    file_list = []
    word_found = False

    for filename in os.scandir('grunio'):
        if filename.is_file():
            with open(filename.path, 'r') as file:
                if word_found:
                    print('\n\n#####################################')
                    word_found = False
                i = 0
                index = 0
                text = file.read().split()
                for word in text:
                    index += 1
                    if word in words:
                        i += 1
                        file_list.append(filename.path)
                        word_found = True
                        print('\n')
                        print(file.name + ' - wystąpienie ' + str(i) + ':')
                        if index-3 < 0 or index-2 < 0 or index-1 < 0:
                            print(' '.join(text[0:index+2]))
                        elif index+1 > len(text) or index+2 > len(text):
                            print(' '.join(text[index-3:index]))
                        else:
                            print(' '.join(text[index-3:index+2]))

    print('\n')
    print('Słowo ' + str(word_input) + ' znajduje się w ' + str(len(set(file_list))) + ' tekstach:')
    print(set(file_list))
    print('\n')

    '''
    for sentence in tokenize.sent_tokenize(text):
        if sentence in words:
            i += 1
            w = [s for s in sentence if s in words]
            if w:
                # sentence = sentence.split(' ')
                file_list.append(filename.path)
                word_found = True
                print('\n')
                print(file.name + ' - zdanie ' + str(i) + ':')
                print(sentence)
    '''


# https://wierzba.wzks.uj.edu.pl/~mgodny/aei/?page_id=13

korkondancja()
