# -*- coding: utf-8 -*-
def get_slug_data():
    return {
        'а': 'a',
        'ә': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'ғ': 'gh',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'j',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'қ': 'q',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'ң': 'ng',
        'о': 'o',
        'ө': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': '',
        'ұ': '',
        'ү': '',
        'ф': 'f',
        'х': 'kh',
        'һ': 'h',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sh',
        'ъ': '',
        'ы': 'y',
        'і': 'i',
        'ь': '',
        'э': 'e',
        'ю': 'i',
        'я': 'ya',
        ' ': '-',
    }


def get_slug_data_for_letter():
    letters = get_slug_data()
    letters2 = {
        'ә': 'ia',
        'ө': 'oi',
        'ұ': 'uw',
        'ү': 'uy',
        'ш': 'sh',
        'щ': 'shh',
        'ы': 'yi',
        'э': 'ie',
    }

    letters.update(letters2)

    return letters


def make_slug(string):
    letters = get_slug_data()
    string = string.strip().lower()
    result = ''

    for l in string:
        if l in letters:
            result += letters[l]
        else:
            result += l

    return result
