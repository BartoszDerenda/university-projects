import os

import math
import re

from clp3 import clp


def _words_from_line(line):
    "Zwraca listę słów dla linijki tekstu."
    words = re.split('[\W\d]+', line)
    return [w.lower() for w in words if w]

def _sort_stat(stat):
    "Sortuje malejąco listę par według drugiego elementu."
    return sorted(stat, key=lambda p: p[1], reverse=True)

def _make_ngram(word, n):
    ngrams = {}

    for i in range(len(word) - n + 1):
        ngram = word[i:i + n]
        if ngram not in ngrams:
            ngrams[ngram] = 0
        ngrams[ngram] += 1

    return ngrams

#input_folder = 'inputs/'
#output_folder = 'outputs/'


def _word_pairs_window_old(array_of_words, word_1, word_2, range_limit):
    count = 0
    index = 0
    last_index_word_1 = None
    last_index_word_2 = None

    for index, word in enumerate(array_of_words):
        if word == word_1:
            last_index_word_1 = index
        if word == word_2:
            last_index_word_2 = index

        if last_index_word_1 is not None and word == word_2 and index - last_index_word_1 <= range_limit:
            count += 1
        if last_index_word_2 is not None and word == word_1 and index - last_index_word_2 <= range_limit:
            count += 1

    return count, index


def _word_pairs_window(array_of_words, word_1, word_2, range_limit):
    count = 0
    number_of_windows = 0

    for i in range(0, len(array_of_words) - range_limit):
        number_of_windows += 1
        if word_1 in array_of_words[i:i+range_limit] and word_2 in array_of_words[i:i+range_limit]:
            count += 1
            #print(word_1, word_2)
            #print(array_of_words[i:i+range_limit])

    return count, number_of_windows


def _base_word(word):
    base_word = word
    id = clp.rec(word)
    if id:
        base_word = clp.bform(id[0])

    return base_word


def mi(input):

    files_dict = {}
    for filename in os.listdir(input):
        if filename.endswith('.txt'):
            with open(os.path.join(input, filename), encoding='utf8') as file:
                text = file.read()

                # Tworzenie listy frekwencyjnej
                word_array = []
                frequency_list = {}
                for word in _words_from_line(text):
                    base_word = _base_word(word)
                    word_array.append(base_word)
                    if base_word not in frequency_list:
                        frequency_list[base_word] = 0
                    frequency_list[base_word] += 1

                file.close()

                # Sprawdzanie wszystkie x wszystkie słowa w danym okienku (defaultowo 5)
                word_count = len(word_array)
                word_pairs = {}
                for base_word_1 in frequency_list:
                    word_pairs.update({base_word_1: {}})
                    for base_word_2 in frequency_list:
                        if base_word_1 != base_word_2:
                            count, number_of_windows = _word_pairs_window(word_array, base_word_1, base_word_2, 5)
                            if count > 15:
                                # print(str(count) + ' / ' + str(number_of_windows))
                                word_pairs[base_word_1][base_word_2] = count/number_of_windows # -> pxy

                # Matematyka wololo
                result = []
                for base_word_1, siblings in word_pairs.items():
                    px = frequency_list[base_word_1] / word_count
                    for base_word_2, pxy in siblings.items():
                        py = frequency_list[base_word_2] / word_count
                        lxy = math.log2(pxy/(px*py))
                        result.append([round(lxy, 1), pxy, frequency_list[base_word_1], px, base_word_1, frequency_list[base_word_2], py, base_word_2, word_count])

                result.sort(reverse=True)
                filtered_result = result[:50]
                print(filename)
                for item in filtered_result:
                    print(item)
                print('\n')
                files_dict.update({filename: filtered_result})


    #with open(output_folder + output, 'w') as file:
    #    file.write('MI \t\t f(x,y) \t f(x) \t x \t\t f(y) \t\t y \n\n')
    #    for item in result:
    #        file.write(str(item[0]) + '\t\t' + str(item[1]) + '\t\t' + str(item[2]) + '\t\t' + str(item[3]) + '\t\t' + str(item[4]) + '\t\t' + str(item[5]))
    #        file.write('\n')
    #
    #    file.close()

    #with open(output_folder + output, 'w') as file:
    #    for word_1, siblings in clean_word_pairs.items():
    #        file.write(str(word_1) + '\n')
    #        for word_2, count in siblings.items():
    #            file.write(str(word_2) + ' - ' + str(word_1) + ' : ' + str(count) + '\n')
    #        file.write('\n\n')


# https://wierzba.wzks.uj.edu.pl/~mgodny/aei/?page_id=29

mi('grunio')
