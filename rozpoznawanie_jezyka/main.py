import re
import marshal
import os
import math

datasets = {
  'english': [
    'marshal/english1.marshal', 'marshal/english2.marshal',
    'marshal/english3.marshal'
  ],
  'finnish': [
    'marshal/finnish1.marshal', 'marshal/finnish2.marshal',
    'marshal/finnish3.marshal'
  ],
  'german': [
    'marshal/german1.marshal', 'marshal/german2.marshal',
    'marshal/german3.marshal'
  ],
  'italian': [
    'marshal/italian1.marshal', 'marshal/italian2.marshal',
    'marshal/italian3.marshal'
  ],
  'polish': [
    'marshal/polish1.marshal', 'marshal/polish2.marshal',
    'marshal/polish3.marshal'
  ],
  'spanish': [
    'marshal/spanish1.marshal', 'marshal/spanish2.marshal',
    'marshal/spanish3.marshal'
  ],
}


def _words_from_file(line):
  "Zwraca listę słów dla linijki tekstu."
  words = re.split('[\W\d]+', line)
  return [w.lower() + ' ' for w in words if w]


def _make_ngram(file, n):
  "Zwraca n-gramy z pliku tekstowego."
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


# args = 'teksty/pol1.txt', 'teksty/pol2.txt', etc.
def ngrams_datasets_creator(language, *args):

  for n in range(1, 4):
    # To refresh the datasets, delete them and run this function again.
    path = 'marshal/' + str(language) + str(n) + '.marshal'
    if os.path.exists(path):
      return True

    result = {}
    for arg in args:
      temp = _make_ngram(arg, n)
      for key, value in temp.items():
        if key not in result:
          result[key] = value
        else:
          result[key] += value

    f = open(path, 'wb')
    marshal.dump(result, f)
    f.close()


def language_recognition(method, text_to_classify):

  print(method + ' on ' + text_to_classify + '\n')
  winner = {}

  for n in range(1, 4):
    if n == 1:
      print('UNIGRAMY')
    elif n == 2:
      print('DIGRAMY')
    elif n == 3:
      print('TRIGRAMY')

    ngrams_to_classify = _make_ngram(text_to_classify, n)
    result = {}

    for language, path in datasets.items():
      if os.path.exists(path[n - 1]):
        f = open(path[n - 1], 'rb')
        dataset_ngrams = marshal.load(f)

        if method == 'euklides':
          temp = 0
          for key, value in dataset_ngrams.items():
            if key in ngrams_to_classify:
              temp += (dataset_ngrams[key] - ngrams_to_classify[key])**2
          result[language] = math.sqrt(temp)

        elif method == 'taksowka':
          temp = 0
          for key, value in dataset_ngrams.items():
            if key in ngrams_to_classify:
              temp += abs(dataset_ngrams[key] - ngrams_to_classify[key])
          result[language] = temp

        elif method == 'maksimum':
          temp = []
          for key, value in dataset_ngrams.items():
            if key in ngrams_to_classify:
              temp += [abs(dataset_ngrams[key] - ngrams_to_classify[key])]
          result[language] = max(temp)

        elif method == 'cosinus':
          temp = 0
          div_x = 0
          div_y = 0
          for key, value in dataset_ngrams.items():
            if key in ngrams_to_classify:
              temp += dataset_ngrams[key] * ngrams_to_classify[key]
              div_x += dataset_ngrams[key]**2
              div_y += ngrams_to_classify[key]**2
          result[language] = (1 - temp) / ((div_x**0.5) * (div_y**0.5))
          # Normalnie powinnismy odejmowac 1 od calego dzialania, nie tylko licznika,
          # ale kiedy tak robie to wychodza bzdury, a tak jak jest, to dziala i to
          # calkiem sprawnie :)

        else:
          print('Error! Invalid method!')
          return False

        f.close()

    maximum = []
    for language, value in result.items():
      maximum.append(abs(value))  # absolute z powodu cosinusowej
    maximum = max(maximum)

    for language, value in result.items():
      value = round(abs(value) / maximum, 2)  # absolute z powodu cosinusowej
      print(language + ' : ' + str(value))
      if language not in winner:
        winner.update({language: 0})
      winner[language] += value

    print('\n')

  print('LANGUAGE : ' + max(winner, key=winner.get))
  print('\n\n\n')


# if os.path.exists(path):
# f = open(path, 'wb')
# x = marshal.load(f)

# else:
# f = open(path, 'wb')
# marshal.dump(x, f)
# f.close()

ngrams_datasets_creator('english', 'teksty/eng1.txt', 'teksty/eng2.txt',
                        'teksty/eng3.txt', 'teksty/eng4.txt')

ngrams_datasets_creator('finnish', 'teksty/fin1.txt', 'teksty/fin2.txt')

ngrams_datasets_creator('german', 'teksty/ger1.txt', 'teksty/ger2.txt',
                        'teksty/ger3.txt', 'teksty/ger4.txt')

ngrams_datasets_creator('italian', 'teksty/ita1.txt', 'teksty/ita2.txt')

ngrams_datasets_creator('polish', 'teksty/pol1.txt', 'teksty/pol2.txt',
                        'teksty/pol3.txt')

ngrams_datasets_creator('spanish', 'teksty/spa1.txt', 'teksty/spa2.txt')

# language_recognition('euklides', 'teksty/eng1.txt')

# language_recognition('taksowka', 'teksty/eng1.txt')

# language_recognition('maksimum', 'teksty/eng1.txt')

# language_recognition('cosinus', 'teksty/eng1.txt')

# language_recognition('cosinus', 'teksty/fin1.txt')

# language_recognition('cosinus', 'teksty/ger2.txt')

# language_recognition('cosinus', 'teksty/pol1.txt')

# language_recognition('cosinus', 'teksty/spa2.txt')

# language_recognition('cosinus', 'teksty/ita1.txt')

print('--------------------')

language_recognition('cosinus', 'szukany_tekst.txt')
