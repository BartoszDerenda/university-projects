import csv
import marshal

from clp3 import clp
import os
import re

def _words_from_line(line):
    "Zwraca listę słów dla linijki tekstu."
    words = re.split('[\W\d]+', line)
    return [w.lower() for w in words if w]

def create_frequency_list():
    input_directory = 'core_text_files'
    output_filename = 'frequency_list.marshal'
    frequency_list = {}

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf8') as current_file:

                text = current_file.read()
                word_array = _words_from_line(text)
                for word in word_array:
                    id = clp.rec(word)
                    if id:
                        word = clp.bform(id[0])
                        if word not in frequency_list:
                            frequency_list[word] = 0
                        frequency_list[word] += 1

            current_file.close()

    frequency_list_trimmed = {}
    for key, value in frequency_list.items():
        if value >= 5:
            frequency_list_trimmed.update({key: value})

    sorted_frequency_list = sorted(frequency_list_trimmed.items(), key=lambda item: item[1], reverse=True)

    with open(output_filename, 'wb') as file:
        marshal.dump(sorted_frequency_list, file)


create_frequency_list()