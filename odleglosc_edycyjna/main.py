# diak1 = ['a', 'c', 's', 'l', 'o', 'n', 'z']
# diak2 = ['ą', 'ć', 'ś', 'ł', 'ó', 'ń', 'ż', 'ź']

# orto_dig_rz = ['rz', 'ch', 'om', 'em']
# orto_dig_z = ['ż', 'h', 'ą', 'ę']
# orto_uni1 = ['u']
# orto_uni2 = ['ó']

orto = {'rz': 'ż', 'ch': 'h', 'om': 'ą', 'em': 'ę', 'u': 'ó'}
diak = {
    'ą': 'a',
    'ć': 'c',
    'ś': 's',
    'ł': 'l',
    'ó': 'o',
    'ń': 'n',
    'ż': 'z',
    'ź': 'z'
}


def modlevenstein(word1, word2):
  # Builds the template matrix based off two words
  matrix = [[0 for x in range(len(word1) + 1)] for x in range(len(word2) + 1)]
  # matrix = [list(range(len(word1) + 1))] * (len(word2) + 1)

  for i in range(0, len(word2) + 1):
    matrix[i][0] = i

  for i in range(0, len(word1) + 1):
    matrix[0][i] = i

  # Levenshtein operations
  for x in range(1, len(word2) + 1):
    for y in range(1, len(word1) + 1):
      # Jeżeli literki są takie same
      if word1[y - 1] == word2[x - 1]:
        matrix[x][y] = matrix[x - 1][y - 1]
        # print(matrix[x][y])

      else:
        diakretyk = 999
        ortograf = 999
        czeski = 999

        # NIE DZIAŁA
        # Oblicza wagę dla czeskiego błędu
        if y < len(word1) and x < len(word2):
          if word1[y - 1] == word2[x]:
            czeski = matrix[x - 1][y - 1] + 0.5
          if word1[y] == word2[x - 1]:
            czeski = matrix[x - 1][y - 1] + 0.5
            matrix[x + 1][y + 1] = czeski

        # Działa tylko dla "ó - u"
        # Oblicza wagę dla błędów ortograficznych
        if y < len(word1) and x < len(word2):
          for key, value in orto.items():
            if (word1[y - 1] + word1[y] == key and word2[x - 1] == value or \
            word1[y - 1] == value and word2[x - 1] + word2[x] == key) \
            or \
            (word1[y - 1] == key and word2[x - 1] == value or \
            word1[y - 1] == value and word2[x - 1] == key):
              # print(word1[y - 1] + word1[y])
              # print(word2[x - 1])
              ortograf = matrix[x - 1][y - 1] + 0.5
              matrix[x + 1][y + 1] = ortograf

        # Oblicza wagę dla błędów diakretycznych
        for key, value in diak.items():
          if (word1[y - 1] == key and word2[x - 1] == value) or \
          (word1[y - 1] == value and word2[x - 1] == key):
            diakretyk = matrix[x - 1][y - 1] + 0.2
            if word1[y - 1] == 'ż' and word2[x - 1] == 'z':
              if x - 2 >= 0 and word2[x - 2] == 'r':
                diakretyk = matrix[x - 1][y]
            elif word1[y - 1] == 'z' and word2[x - 1] == 'ż':
              if y - 2 >= 0 and word1[y - 2] == 'r':
                diakretyk = matrix[x][y - 1]

        # Oblicza wagę dla edycji
        edit = matrix[x - 1][y - 1] + 1

        # Oblicza wagę dla usunięcia
        deletion = matrix[x][y - 1] + 1

        # Oblicza wagę dla wstawienia
        insertion = matrix[x - 1][y] + 1

        if matrix[x][y] != 0:
          matrix[x][y] = min(matrix[x][y], czeski, diakretyk, ortograf, edit,
                             deletion, insertion)
        else:
          matrix[x][y] = min(czeski, diakretyk, ortograf, edit, deletion,
                             insertion)
    #print(min(matrix[x]))

  print('ROZWIAZANIE')
  for item in matrix:
    print('\n')
    for dec in item:
      print(f'{dec}\t\t', end='')

  # Returns last value in matrix
  print('\n')
  print(word1)
  print(word2)

  return matrix[len(word2)][len(word1)]


###############################################

print(modlevenstein('pierze', 'pieże'))  # 0.5 [x]
print('\n')
print(modlevenstein('smiech', 'śmiech'))  # 0.2 [x]
print('\n')
print(modlevenstein('piora', 'piórą'))  # 0.4 [x]
print('\n')
print(modlevenstein('piura', 'pióra'))  # 0.5 [x]
print('\n')
print(modlevenstein('człowiek', 'cłzoiwek'))  # 1.0
print('\n')
print(modlevenstein('zrobić', 'rzobić'))  # 0.5 [x]
print('\n')
print(modlevenstein('zima', 'źima'))  # 0.2 [x]
print('\n')
print(modlevenstein('prosiłem', 'prsoilem'))  # 0.7 [x]
print('\n')
print(modlevenstein('ćwok', 'wciok'))  # 2.2 [x]
print('\n')
print(modlevenstein('wciok', 'ćwok'))  # 2.2 [x]
print('\n')
print(modlevenstein('elo', 'leo'))  # 0.5 [x]
print('\n')
print(modlevenstein('leo', 'elo'))  # 0.5 [x]

# wynik:
# 0
# 1
# 3
# 4
