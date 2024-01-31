import re


def _words_from_file(line):
  "Zwraca listę słów dla linijki tekstu."
  words = re.split('[\W\d]+', line)
  return [w.lower() + ' ' for w in words if w]


def ngram(file, n):

  with open(file, 'r') as f:
    text = f.read()

    ngrams = {}
    i = 0

    # print(_words_from_file(text))
    for word in _words_from_file(text):
      for i in range(len(word) - n + 1):
        ngram = word[i:i + n]
        if ngram not in ngrams:
          ngrams[ngram] = 0
        ngrams[ngram] += 1

    return ngrams


print(ngram('pol1.txt', 2))

# for symbol in word:
# symbol_array.append(symbol)

# for x in range(len(symbol_array)):
# print(symbol_array[x])

# print(len(symbol_array))
# print(symbol_array)

# ngrams = {}
# for symbol in symbol_array:
# print(symbol_array.index(symbol))

# ngram = ''
# index = symbol_array.index(symbol)

# for i in range(index, index + n):
# ngram += symbol_array[i]

# if ngram not in ngrams:
# ngrams[ngram] = 0
# ngrams[ngram] += 1
# print(ngram)

# print(ngrams)
