def longest_common_subsequence(s1, s2):

  matrix = [[x for x in range(len(s1) + 1)] for x in range(len(s2) + 1)]
  # matrix = [list(range(len(word1) + 1))] * (len(word2) + 1)
  for i in range(0, len(s2) + 1):
    matrix[i][0] = 0

  for i in range(0, len(s1) + 1):
    matrix[0][i] = 0

  print(s1 + ' --- ' + s2)

  for x in range(1, len(s2) + 1):
    for y in range(1, len(s1) + 1):
      if s1[y - 1] == s2[x - 1]:
        matrix[x][y] = matrix[x - 1][y - 1] + 1
      else:
        matrix[x][y] = max(matrix[x - 1][y], matrix[x][y - 1])

  print('\n')
  print('ROZWIAZANIE')
  for array in matrix:
    print('\n')
    for item in array:
      print(f'{item}\t', end='')

  result = min(matrix[len(s2)][len(s1)] / len(s1),
               matrix[len(s2)][len(s1)] / len(s2))

  return result


print(longest_common_subsequence('ABBA', 'AABABA'))
print('\n\n\n\n')
print(longest_common_subsequence('AAACA', 'ACAAA'))
print('\n\n\n\n')
print(longest_common_subsequence('AABBCCAA', 'ABCAA'))
print('\n\n\n\n')
print(longest_common_subsequence('POLITECHNIKA', 'TOALETA'))
