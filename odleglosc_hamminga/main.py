def hamming(word, comparison):
  if len(word) != len(comparison):
    return 'Please input two words of the same length.'

  count = 0
  for i in range(len(word)):
    if word[i] != comparison[i]:
      count += 1

  return count


print(hamming('pies', 'pies'))
print(hamming('granat', 'granit'))
print(hamming('1001010', '1011011'))
print(hamming('abcd', 'dcba'))
print(hamming('abcd', 'abdc'))
