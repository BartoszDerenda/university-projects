import re
import csv
import math
import os
from clp3 import clp
from collections import defaultdict


def _words_from_line(line):
    "Zwraca listę słów dla linijki tekstu."
    words = re.split('[\W\d]+', line)
    return [w.lower() for w in words if w]


def _sort_stat(stat):
    "Sortuje malejąco listę par według drugiego elementu."
    return sorted(stat, key=lambda p: p[1], reverse=True)


def tfidf():

    directory = input("Please input the path to a directory with text samples: ")

    number_of_files = 0
    file_number = 0
    global_result = {}
    tf_dict = {}
    idf_dict = {}

    for filename in os.scandir(directory):
        if filename.is_file():
            number_of_files += 1

    for filename in os.scandir(directory):
        if filename.is_file():
            file_number += 1
            result = {}
            checked_words = []
            with open(filename.path, 'r') as f:
                text = f.read()

                word_count = 0
                for line in _words_from_line(text):
                    id = clp.rec(line)
                    if id:
                        word = clp.bform(id[0])
                        if word not in result:
                            result[word] = 0
                        if word not in global_result:
                            global_result[word] = 1
                            checked_words.append(word)
                        if word not in checked_words:
                            global_result[word] += 1
                            checked_words.append(word)
                        result[word] += 1
                        word_count += 1

            temp = {}
            for key, value in result.items():
                tf = value / word_count
                temp[key] = tf

            tf_dict[filename.path] = temp
            f.close()

    temp = {}
    for filename, data in tf_dict.items():
        for key, value in data.items():
            if key in global_result:
                idf = math.log((number_of_files / global_result[key]), 10)
                temp[key] = idf
        idf_dict[filename] = temp


    """  N^4 shenanigans :)  """
    """  How do I map 2D dictionaries to each other help  """
    supreme_result = {}
    for filename, idf in idf_dict.items():
        for filename2, tf in tf_dict.items():
            if filename == filename2:
                supreme_result[filename] = {}
                for key, value in idf.items():
                    for key2, value2 in tf.items():
                        if key == key2:
                            x = value * value2
                            supreme_result[filename][key] = x

    # with open('wynik_' + directory + '.csv', 'w') as csvfile:
       # writer = csv.DictWriter(csvfile, fieldnames='grunio')
       # writer.writeheader()
       # writer.writerows(supreme_result)



    output = open('wynik_' + directory + '.csv', 'w')
    writer = csv.writer(output)
    for item, value in supreme_result.items():
        row = ['\n' + item + ',']
        writer.writerow(row)

        x = _sort_stat(value.items())
        for i in range(0, 10):
            row = [str(x[i][0]) + ',' + str(round(x[i][1], 4))]
            writer.writerow(row)

    output.close()


tfidf()
