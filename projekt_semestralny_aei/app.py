from flask import Flask, render_template
import os
import re
import marshal

from clp3 import clp

app = Flask(__name__, template_folder='templates')

obiekt_list = ['świnka', 'sierść', 'gryzoń', 'pupil', 'kawia']
narzedzie_list = ['warzywo', 'owoc', 'woda', 'witamina', 'sianko', 'siano', 'zabawka', 'karma']
miejsce_list = ['klatka', 'hodowla', 'domek', 'teren', 'wybieg', 'ściółka']

sprawca_list = ['opiekun', 'weterynarz', 'właściciel', 'hodowca']
zdarzenie_list = ['dieta', 'zakup']
cel_list = ['jeść', 'opieka', 'pielęgnacja']

wagi = {
() : 0,
('cel',) : 0.1,
('miejsce',) : 0.1,
('narzedzie',) : 0.15,
('obiekt',) : 0.1,
('sprawca',) : 0.1,
('zdarzenie',) : 0.1,
('cel', 'miejsce') : 0.2,
('cel', 'narzedzie') : 0.2,
('cel', 'obiekt') : 0.25,
('cel', 'sprawca') : 0.2,
('cel', 'zdarzenie') : 0.15,
('miejsce', 'narzedzie') : 0.25,
('miejsce', 'obiekt') : 0.35,
('miejsce', 'sprawca') : 0.25,
('miejsce', 'zdarzenie') : 0.2,
('narzedzie', 'obiekt') : 0.25,
('narzedzie', 'sprawca') : 0.2,
('narzedzie', 'zdarzenie') : 0.2,
('obiekt', 'sprawca') : 0.35,
('obiekt', 'zdarzenie') : 0.25,
('sprawca', 'zdarzenie') : 0.15,
('cel', 'miejsce', 'narzedzie') : 0.4,
('cel', 'miejsce', 'obiekt') : 0.65,
('cel', 'miejsce', 'sprawca') : 0.45,
('cel', 'miejsce', 'zdarzenie') : 0.45,
('cel', 'narzedzie', 'obiekt') : 0.65,
('cel', 'narzedzie', 'sprawca') : 0.45,
('cel', 'narzedzie', 'zdarzenie') : 0.45,
('cel', 'obiekt', 'sprawca') : 0.65,
('cel', 'obiekt', 'zdarzenie') : 0.65,
('cel', 'sprawca', 'zdarzenie') : 0.45,
('miejsce', 'narzedzie', 'obiekt') : 0.85,
('miejsce', 'narzedzie', 'sprawca') : 0.45,
('miejsce', 'narzedzie', 'zdarzenie') : 0.45,
('miejsce', 'obiekt', 'sprawca') : 0.7,
('miejsce', 'obiekt', 'zdarzenie') : 0.7,
('miejsce', 'sprawca', 'zdarzenie') : 0.45,
('narzedzie', 'obiekt', 'sprawca') : 0.7,
('narzedzie', 'obiekt', 'zdarzenie') : 0.65,
('narzedzie', 'sprawca', 'zdarzenie') : 0.45,
('obiekt', 'sprawca', 'zdarzenie') : 0.65,
('cel', 'miejsce', 'narzedzie', 'obiekt') : 0.9,
('cel', 'miejsce', 'narzedzie', 'sprawca') : 0.7,
('cel', 'miejsce', 'narzedzie', 'zdarzenie') : 0.6,
('cel', 'miejsce', 'obiekt', 'sprawca') : 0.85,
('cel', 'miejsce', 'obiekt', 'zdarzenie') : 0.8,
('cel', 'miejsce', 'sprawca', 'zdarzenie') : 0.7,
('cel', 'narzedzie', 'obiekt', 'sprawca') : 0.85,
('cel', 'narzedzie', 'obiekt', 'zdarzenie') : 0.85,
('cel', 'narzedzie', 'sprawca', 'zdarzenie') : 0.75,
('cel', 'obiekt', 'sprawca', 'zdarzenie') : 0.85,
('miejsce', 'narzedzie', 'obiekt', 'sprawca') : 0.9,
('miejsce', 'narzedzie', 'obiekt', 'zdarzenie') : 0.9,
('miejsce', 'narzedzie', 'sprawca', 'zdarzenie') : 0.8,
('miejsce', 'obiekt', 'sprawca', 'zdarzenie') : 0.8,
('narzedzie', 'obiekt', 'sprawca', 'zdarzenie') : 0.8,
('cel', 'miejsce', 'narzedzie', 'obiekt', 'sprawca') : 0.95,
('cel', 'miejsce', 'narzedzie', 'obiekt', 'zdarzenie') : 0.95,
('cel', 'miejsce', 'narzedzie', 'sprawca', 'zdarzenie') : 0.8,
('cel', 'miejsce', 'obiekt', 'sprawca', 'zdarzenie') : 0.9,
('cel', 'narzedzie', 'obiekt', 'sprawca', 'zdarzenie') : 0.9,
('miejsce', 'narzedzie', 'obiekt', 'sprawca', 'zdarzenie') : 0.95,
('cel', 'miejsce', 'narzedzie', 'obiekt', 'sprawca', 'zdarzenie') : 1
}

def _words_only(text):
    "Zwraca listę słów dla linijki tekstu."
    words = re.split('[\W\d]+', text)
    return [w.lower() for w in words if w]

def _words_and_punctuation(text):
    "Zwraca liste słów oraz znaków specjalnych."
    matches = re.findall(r'\w+|[^\w\s]', text)
    return matches

def _reconstruct_text(word_array):
    output = ' '
    for word in word_array:
        if word not in ('.', ',', '—', '!', '?', ')', ']', '}', '%'):
            if output[-1] not in ('(', '[', '{'):
                output += ' '
        output += word
    return output[1:]


@app.route('/')
def homepage():
    dir = 'text_files'
    cache = 'cache.marshal'
    output = {}

    if os.path.exists(cache):
        with open(cache, 'rb') as file:
            output = marshal.load(file)

    else:

        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf8') as current_file:

                    rating = 0
                    text = current_file.read()
                    real_word_array = _words_and_punctuation(text)
                    modified_word_array = []
                    frequency_count = {'sprawca': [], 'zdarzenie': [], 'obiekt': [], 'narzedzie': [], 'miejsce': [], 'cel': []}
                    sprawca = False
                    zdarzenie = False
                    obiekt = False
                    narzedzie = False
                    miejsce = False
                    cel = False

                    for word in real_word_array:

                        base_word = word
                        id = clp.rec(word)
                        if id:
                           base_word = clp.bform(id[0])

                        if base_word in sprawca_list:
                            sprawca = True
                            modified_word = '<span class="sprawca">' + str(word) + '</span>'
                            frequency_count['sprawca'].append(base_word)
                        elif base_word in zdarzenie_list:
                            zdarzenie = True
                            modified_word = '<span class="zdarzenie">' + str(word) + '</span>'
                            frequency_count['zdarzenie'].append(base_word)
                        elif base_word in obiekt_list:
                            obiekt = True
                            modified_word = '<span class="obiekt">' + str(word) + '</span>'
                            frequency_count['obiekt'].append(base_word)
                        elif base_word in narzedzie_list:
                            narzedzie = True
                            modified_word = '<span class="narzedzie">' + str(word) + '</span>'
                            frequency_count['narzedzie'].append(base_word)
                        elif base_word in miejsce_list:
                            miejsce = True
                            modified_word = '<span class="miejsce">' + str(word) + '</span>'
                            frequency_count['miejsce'].append(base_word)
                        elif base_word in cel_list:
                            cel = True
                            modified_word = '<span class="cel">' + str(word) + '</span>'
                            frequency_count['cel'].append(base_word)
                        else:
                            modified_word = word
                        modified_word_array.append(modified_word)

                    temp = []
                    if cel:
                        temp.append('cel')
                    if miejsce:
                        temp.append('miejsce')
                    if narzedzie:
                        temp.append('narzedzie')
                    if obiekt:
                        temp.append('obiekt')
                    if sprawca:
                        temp.append('sprawca')
                    if zdarzenie:
                        temp.append('zdarzenie')

                    rating = wagi[tuple(temp)]
                    rating = round(rating, 2)
                    rating = int(rating*100)
                    text = _reconstruct_text(modified_word_array)

                    frequency_context = {}
                    for item, value in frequency_count.items():
                        frequency_context.update({item: set(value)})

                    # Save the filename as int so that it is easier to sort in Jinja2.
                    # Just add '.txt' to the HTML file when you display it.
                    filename = int(filename.split('.', 1)[0])

                    output.update({filename: [text, rating, frequency_context]})
                current_file.close()

        with open(cache, 'wb') as file:
            marshal.dump(output, file)


    return render_template('homepage.html', output=output)


@app.route('/lista_frekwencyjna')
def frequency_list():
    return render_template('frequency_list.html', sprawca_list=sprawca_list, cel_list=cel_list,
                           obiekt_list=obiekt_list, zdarzenie_list=zdarzenie_list, miejsce_list=miejsce_list,
                           narzedzie_list=narzedzie_list)

@app.route('/wagi')
def weights():
    return render_template('weights.html', weights=wagi)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=12006, debug=True)