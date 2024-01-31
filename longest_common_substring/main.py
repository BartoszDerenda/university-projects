def longest_common_substring(s1, s2):

  lmax = 0
  for y in range(0, len(s2)):
    for x in range(0, len(s1)):
      lm = 0
      while s2[y + lm] == s1[x + lm]:
        lm += 1
        if y + lm == len(s2) or x + lm == len(s1):
          break
      if lm > lmax:
        lmax = lm

  return min(lmax / len(s1), lmax / len(s2))


print(longest_common_substring('ABBA', 'AABABA'))  # 2/6 (AB / BA)
print('\n\n')
print(longest_common_substring('AAACA', 'ACAAA'))  # 3/5 (AAA)
print('\n\n')
print(longest_common_substring('AABBCCAA', 'ABCAA'))  # 3/8 (CAA)
print('\n\n')
print(longest_common_substring('POLITECHNIKA', 'POLKA'))  # 3/12 (POL)
