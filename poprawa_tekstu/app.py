import re
import marshal
import os
import csv

"""Potrzebne do modlevenstein()"""
orto = {"rz": "ż",
        "ch": "h",
        "om": "ą",
        "em": "ę",
        "u": "ó"
        }

diak = {"ą": "a",
        "ć": "c",
        "ś": "s",
        "ł": "l",
        "ó": "o",
        "ń": "n",
        "ż": "z",
        "ź": "z"
        }


def _words_from_file(line):
    """Zwraca listę słów dla linijki tekstu."""
    words = re.split("[\W\d]+", line)
    return [w.lower() for w in words if w]


def _sort_stat(stat):
    """Sortuje malejąco listę par według drugiego elementu."""
    return sorted(stat, key=lambda p: p[1], reverse=True)


def _serialize_dataset(path):
    """Krótka funkcja służąca do przerobienia SJP na wersję bitową"""
    if os.path.exists(path):
        return True
    result = []
    f_in = open("odm.txt", "r")
    for line in f_in:
        for word in _words_from_file(line):
            result.append(word)

    f_out = open(path, "wb")
    marshal.dump(result, f_out)
    f_in.close()
    f_out.close()


_serialize_dataset("odm.marshal")


def frequency_list(file):
    """Useless"""
    result = {}
    output = open("result.csv", "w")
    with open(file, "r") as f:
        text = f.read()

        for word in _words_from_file(text):
            if word not in result:
                result[word] = 0
            result[word] += 1

    x = _sort_stat(result.items())

    writer = csv.writer(output)
    i = 0
    for key, value in x:
        i += 1
        row = [str(i) + " " + str(key) + " " + str(value)]
        writer.writerow(row)

    f.close()
    output.close()


def modlevenstein(word1, word2, current_max):
    """Tworzy matrycę"""
    matrix = [[0 for x in range(len(word1) + 1)] for x in range(len(word2) + 1)]

    """Zeruje wnętrze matrycy"""
    for i in range(0, len(word2) + 1):
        matrix[i][0] = i
    for i in range(0, len(word1) + 1):
        matrix[0][i] = i

    for x in range(1, len(word2) + 1):
        for y in range(1, len(word1) + 1):

            """Jeżeli literki są takie same..."""
            if word1[y - 1] == word2[x - 1]:
                matrix[x][y] = matrix[x - 1][y - 1]

            else:
                diakretyk = 999
                ortograf = 999
                czeski = 999

                """Oblicza wagę dla czeskiego błędu"""
                if y < len(word1) and x < len(word2):
                    if word1[y - 1] == word2[x]:
                        czeski = matrix[x - 1][y - 1] + 0.5
                    if word1[y] == word2[x - 1]:
                        czeski = matrix[x - 1][y - 1] + 0.5
                        matrix[x + 1][y + 1] = czeski

                """Oblicza wagę dla błędów ortograficznych"""
                if y < len(word1) and x < len(word2):
                    for key, value in orto.items():
                        if (
                            word1[y - 1] + word1[y] == key
                            and word2[x - 1] == value
                            or word1[y - 1] == value
                            and word2[x - 1] + word2[x] == key
                        ) or (
                            word1[y - 1] == key
                            and word2[x - 1] == value
                            or word1[y - 1] == value
                            and word2[x - 1] == key
                        ):
                            ortograf = matrix[x - 1][y - 1] + 0.5
                            matrix[x + 1][y + 1] = ortograf

                """Oblicza wagę dla błędów diakretycznych"""
                for key, value in diak.items():
                    if (word1[y - 1] == key and word2[x - 1] == value) or (
                        word1[y - 1] == value and word2[x - 1] == key
                    ):
                        diakretyk = matrix[x - 1][y - 1] + 0.2

                        if word1[y - 1] == "ż" and word2[x - 1] == "z":
                            if x - 2 >= 0 and word2[x - 2] == "r":
                                diakretyk = matrix[x - 1][y]

                        elif word1[y - 1] == "z" and word2[x - 1] == "ż":
                            if y - 2 >= 0 and word1[y - 2] == "r":
                                diakretyk = matrix[x][y - 1]

                """Oblicza wagę dla edycji"""
                edit = matrix[x - 1][y - 1] + 1

                """Oblicza wagę dla usunięcia"""
                deletion = matrix[x][y - 1] + 1

                """Oblicza wagę dla wstawienia"""
                insertion = matrix[x - 1][y] + 1

                if matrix[x][y] != 0:
                    matrix[x][y] = min(
                        matrix[x][y],
                        czeski,
                        diakretyk,
                        ortograf,
                        edit,
                        deletion,
                        insertion,
                    )
                else:
                    matrix[x][y] = min(
                        czeski,
                        diakretyk,
                        ortograf,
                        edit,
                        deletion,
                        insertion
                    )

        if min(matrix[x]) > current_max:
            return 999

    return matrix[len(word2)][len(word1)]


def poprawiak():
    text_input = input("Wprowadź tekst: ")
    f = open("odm.marshal", "rb")
    odmiany = marshal.load(f)

    input_array = _words_from_file(text_input)
    # ['Ala', 'ma', 'pjeska', 'bannan']

    input_array_length = len(input_array)
    positive_counter = 0

    playdough = {}
    for word in input_array:
        playdough.update({word: {"placeholder": 999}})
        path = "dataset/" + str(word) + ".marshal"
        if os.path.exists(path):
            playdough.update({word: "marshal"})
            positive_counter += 1
            # 'bannan.marshal' istnieje, także...
            # {'Ala': {'placeholder': 999}, 'ma': {'placeholder': 999}, 'pjeska': {'placeholder': 999}, 'bannan': 'marshal'}

    for line in odmiany:
        if input_array_length == positive_counter:
            break
        for odmiana in _words_from_file(line):

            if odmiana in playdough:
                playdough.update({odmiana: "correct"})
                positive_counter += 1
                # {'Ala': 'correct', 'ma': 'correct', 'pjeska': {'placeholder': 999}, 'bannan': 'marshal'}

            for word, hints in playdough.items():
                if (hints != "correct") and (hints != "marshal"):
                    max_key = max(hints, key=hints.get)
                    max_value = hints[max_key]
                    difference = modlevenstein(word, odmiana, max_value)
                    # ^ cała magia

                    """Jeżeli znajdzie coś, co ma mniejszą wagę levenstaina od obecnego słowa z największą wagą to dodaje"""
                    if difference < max_value:
                        hints.update({odmiana: difference})
                    if len(hints) > 15:
                        del hints[max_key]

    """Zapisuje wcześniej sprawdzone przypadki"""
    for word, hints in playdough.items():
        path = "dataset/" + str(word) + ".marshal"
        if (hints != "correct") and (hints != "marshal"):
            f = open(path, "wb")
            result = {word: hints}
            marshal.dump(result, f)
            f.close()

    for word, hints in playdough.items():
        if hints != "correct":
            print('Wykryto błąd w słowie "' + word + '". Czy miałeś może na myśli...')
            path = "dataset/" + str(word) + ".marshal"
            f = open(path, "rb")
            result = marshal.load(f)
            f.close()

            counter = 0
            for word, hints in result.items():
                for hint, weight in hints.items():
                    counter += 1
                    print(str(counter) + ". " + hint)
            choice = input('Wprowadź słowo: ')

            if choice not in hints:
                difference = modlevenstein(choice, word, 99)
                f = open(path, "wb")
                f.truncate(0)
                for key, value in result.items():
                    value.update({choice: difference})
                marshal.dump(result, f)
                f.close()

            """Updateuje output"""
            i = [
                index for index in range(len(input_array)) if input_array[index] == word
            ]
            input_array[i[0]] = choice

    """Printuje output (nie obsługuje znaków specjalnych bo jestem leniwy)"""
    print("\n" + " ".join(input_array))


poprawiak()
# frequency_list('odm.txt')
