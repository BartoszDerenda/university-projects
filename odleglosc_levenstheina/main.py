def levenshtein(word1, word2):
  # Builds the template matrix based off two words
  matrix = [[x for x in range(len(word1) + 1)] for x in range(len(word2) + 1)]
  for i in range(0, len(word2) + 1):
    matrix[i][0] = i

  # print('TEMPLATE')
  # for item in matrix:
  # print(item)
  # print('\n')

  # Levenshtein operations
  for i in range(1, len(word2) + 1):
    for j in range(1, len(word1) + 1):
      if word1[j - 1] == word2[i - 1]:
        matrix[i][j] = matrix[i - 1][j - 1]
      else:
        edit = matrix[i - 1][j - 1] + 1
        deletion = matrix[i][j - 1] + 1
        insertion = matrix[i - 1][j] + 1
        matrix[i][j] = min(edit, deletion, insertion)
        # print(
        # str(edit) + ' ' + str(deletion) + ' ' + str(insertion) + ' -- ' + str(matrix[i][j])
        # )

  # print('ROZWIAZANIE')
  # for item in matrix:
  # print(item)

  # Returns last value in matrix
  return matrix[len(word2)][len(word1)]


###############################################

print(levenshtein('pies', 'pies'))
print(levenshtein('granat', 'granit'))
print(levenshtein('orczyk', 'oracz'))
print(levenshtein('marka', 'ariada'))
print(levenshtein('abcdefgh', 'defghabc'))

# wynik:
# 0
# 1
# 3
# 4
