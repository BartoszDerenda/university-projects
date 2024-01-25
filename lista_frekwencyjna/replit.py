import re
import csv
from clp3 import clp


def _words_from_line(line):
    "Zwraca listę słów dla linijki tekstu."
    words = re.split('[\W\d]+', line)
    return [w.lower() for w in words if w]


def _sort_stat(stat):
    "Sortuje malejąco listę par według drugiego elementu."
    return sorted(stat, key=lambda p: p[1], reverse=True)


def frequency_list(file):
    result = {}
    output = open('result.csv', 'w')
    with open(file, 'r') as f:
        text = f.read()

        for line in _words_from_line(text):
            id = clp.rec(line)
            if id:
                word = clp.bform(id[0])
                if word not in result:
                    result[word] = 0
                result[word] += 1

    sorted_result = _sort_stat(result.items())

    writer = csv.writer(output)
    i = 0
    x = 0
    for key, value in sorted_result:
        if x < 10:
            x += 1
        else:
            if value > 1:
                i += 1
                row = [str(i) + ' ' + str(key) + ' ' + str(value)]
                writer.writerow(row)

    f.close()
    output.close()

frequency_list('wiki.txt')
