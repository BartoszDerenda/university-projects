polish_dict = {
  'Ą': 'a',
  'ą': 'a',
  'Ć': 'c',
  'ć': 'c',
  'Ę': 'e',
  'ę': 'e',
  'Ł': 'l',
  'ł': 'l',
  'Ń': 'n',
  'ń': 'n',
  'Ó': 'o',
  'ó': 'o',
  'Ś': 's',
  'ś': 's',
  'Ź': 'z',
  'ź': 'z',
  'Ż': 'z',
  'ż': 'z'
}


def caesar_cipher(cipher, key):
  result = []

  for letter in cipher:

    # Zamiana polskich znaków, np. ą -> a
    if letter in polish_dict:
      letter = polish_dict[letter]

    # Zamiana znaków na kod ASCII
    temp = ord(letter)
    letter = ord(letter)

    # Kodowanie + zamiana dużych liter na małe
    if 97 <= letter <= 122:
      letter += key
    elif 65 <= letter <= 90:
      letter += key + 32
    else:
      letter = letter

    # Zapobiegnięcie wychodzenia poza alfabet
    if letter != 32 and ((97 <= temp <= 122) or (65 <= temp <= 90)):
      if letter > 122:
        letter -= 26
      elif letter < 97:
        letter += 26

    result.append(chr(letter))

  print(''.join(result))


caesar_cipher('zzzABCDEFGH a ĄąŻżŹźĆćÓóŁłĘę .,(){}', 1)
caesar_cipher('abcdefgh', 3)
caesar_cipher('zxyZXYoplasd', 3)
caesar_cipher('if (ala ma kota): {"test": 123}', -12)

caesar_cipher('DOD PD NRWD L SLHVHOD.', -3)
