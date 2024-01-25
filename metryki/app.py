import re
import csv
import math
import os
import locale
# import nltk
import marshal
from clp3 import clp
from nltk import tokenize
from collections import defaultdict

locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")
# nltk.download('punkt')

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


def _calculate_cosinus(input_ngrams, dataset_ngrams):
    cos = 0
    div_x = 0
    div_y = 0

    for key in input_ngrams:
        div_x += input_ngrams[key] ** 2

        if key in dataset_ngrams:
            cos += abs(dataset_ngrams[key] * input_ngrams[key])

    for key in dataset_ngrams:
         div_y += dataset_ngrams[key] ** 2

    div_xy = (div_x**0.5) * (div_y**0.5)
    result = abs((cos / div_xy))

    result = round(result, 8)

    """
    print(div_x)
    print(div_y)
    print(str(cos) + ' / ' + str(div_xy))
    print(result)
    """

    return result


def metryka(text):
    playdough = []

    with open(text, 'r') as main_file:

        for line_in_file in main_file:
            line_modified = (''.join(_words_from_line(line_in_file)), line_in_file)
            line_ngram = _make_ngram(line_modified[0], 2)

            if len(playdough) == 0:
                playdough.append([line_modified[1]])
            else:
                comparison = {}
                for cluster in playdough:
                    dataset = ''
                    line_counter = 0
                    for line_in_cluster in cluster:
                        if line_counter < 4:
                            dataset += ''.join(_words_from_line(line_in_cluster))
                            line_counter += 1

                    dataset_ngram = _make_ngram(dataset, 2)
                    temp = _calculate_cosinus(line_ngram, dataset_ngram)
                    comparison.update({playdough.index(cluster): temp})

                    """
                    print('\n')
                    print(line_modified[0])
                    print('v.s.')
                    print(dataset)
                    print('\n')
                    print(line_ngram)
                    print('\n')
                    print(dataset_ngram)
                    z = 0
                    y = 0
                    for x in line_ngram:
                        y += 1
                        if x in dataset_ngram:
                            z += 1
                    print('Matching - ' + str(z) + ' out of ' + str(y))
                    print('\n\n\n\n')
                    """

                max_value = max(comparison.values())
                max_key = max(comparison, key=comparison.get)

                # print(max_value)
                # print('\n\n\n\n')

                if max_value > 0.75:
                    playdough[max_key].append(line_modified[1])
                else:
                    playdough.append([line_modified[1]])


    main_file.close()

    dir = os.listdir('results')
    filename_token = len(dir)
    with open('results/' + str(filename_token) + '_' + str(text), 'w') as result_file:

        for cluster in playdough:
            result_file.write('\n###############################\n\n')
            for row in cluster:
               result_file.write(row)

    """
    directory = 'cache'
    cache_number = 0

    with open(text, 'r') as main_file:
        for line in main_file:
            line = line.rstrip()
            line_ngram = _make_ngram(line, 2)
            # print(line_ngram)

            dir = os.listdir(directory)
            if len(dir) == 0:
                with open(cache_number, 'wb') as cache_file:
                    marshal.dump(line, cache_file)
                    cache_number += 1
                cache_file.close()
                print('\nYYYY')
            else:
                for filename in os.scandir(directory):
                    if filename.is_file():
                        with open(filename.path, 'rb') as cache:
                            playdough = marshal.load(cache)
                            dataset_ngram = _make_ngram(playdough, 2)
                            test = _calculate_cosinus(line_ngram, dataset_ngram)
                            print(test)
                            print('\nXXXX')


                            cache_number += 1

                        cache.close()
    main_file.close()
    """

# https://wierzba.wzks.uj.edu.pl/~mgodny/aei/?page_id=29

metryka('firmy.txt')
