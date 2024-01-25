from clp3 import clp
import itertools

diakret = {"a": "ą", "c": "ć", "n": "ń", "l": "ł", "o": "ó", "s": "ś", "e": "ę"}


def poprawa_clp():

    def get_key(val):
        for key, value in diakret.items():
            if val == value:
                return key
        return False

    word = input('Wprowadź słowo: ')

    playdough = list(word)
    array_of_inputs = [playdough]

    # # # # # # # #
    #              #
    # The "Z" Zone #
    #              #
     # # # # # # # #

    i = 0
    for symbol in word:
        if symbol == "z" or symbol == "ż" or symbol == "ź":
            i += 1

    possibilities = list(itertools.product([0, 1, 2], repeat=i))

    for case in possibilities:
        playdough = list(word)
        i = 0
        for index in range(0, len(word)):

            if word[index] == "z" or word[index] == "ż" or word[index] == "ź":
                if case[i] == 0:
                    playdough[index] = 'z'
                elif case[i] == 1:
                    playdough[index] = 'ż'
                elif case[i] == 2:
                    playdough[index] = 'ź'
                i += 1

        if playdough not in array_of_inputs:
            array_of_inputs.append(playdough)

    # # # # # # # # # # #
    #                   #
    # The "Normal" Zone #
    #                   #
    # # # # # # # # # # #

    i = 0
    for symbol in word:
        if symbol in diakret.keys() or symbol in diakret.values():
            i += 1

    possibilities = list(itertools.product([0, 1], repeat=i))

    output = []
    result = []

    for word in array_of_inputs:
        for case in possibilities:
            playdough = list(word)
            i = 0
            for index in range(0, len(word)):

                if word[index] in diakret.keys() or word[index] in diakret.values():
                    if case[i] == 1:
                        if word[index] in diakret.keys():
                            playdough[index] = diakret[word[index]]

                        elif word[index] in diakret.values():
                            playdough[index] = get_key(word[index])

                    i += 1

            output.append(playdough)

        for item in output:
            modified_item = "".join(item)
            if clp(modified_item) and modified_item not in result:
                result.append(modified_item)

    print(result)




poprawa_clp()