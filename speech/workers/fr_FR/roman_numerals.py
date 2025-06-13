unit = 'I'
five = 'V'
tens = 'X'
fifty = 'L'
hundreds = 'C'
thousands = 'M'

symboles = [
    unit,
    five,
    tens,
    fifty,
    hundreds,
    thousands
]

roman_map = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
    'IV': 4,
    'IX': 9,
    'XL': 40,
    'XC': 90,
    'CD': 400,
    'CM': 900
}

sufix_ponctuation = [' ', '.', ';', ',', '?', '!']
prefix_ponctuation = [
    ' ', '.', ';', ',', '?', '!'
]
prefix_space_ponctuation = [
    ' .', '; ', ', ', '? ', '! '
]


def roman_to_int(roman):
    i = 0
    num = 0
    while i < len(roman):
        if i + 1 < len(roman) and roman[i:i + 2] in roman_map:
            num += roman_map[roman[i:i + 2]]
            i += 2
        else:
            num += roman_map[roman[i]]
            i += 1
    return str(num)


def find_left(text, indice, symbol):
    inc = 1
    while True:
        inc += 1
        if len(text) == indice + inc:
            break
        if text[indice + inc] not in symboles:
            break
    if len(text) != indice + inc and text[indice + inc] == 'e':
        if (
            text[indice + inc + 1] not in sufix_ponctuation
        ):
            return text
        _substr = text[indice + 1:indice + inc + 2]
        if _substr in ['Le ', 'Ce ']:
            return text
        _replace = roman_to_int(text[indice + 1:indice + inc]) + 'ème '
    else:
        if (
            len(text) != indice + inc
            and text[indice + inc] not in sufix_ponctuation
        ):
            return text
        _substr = text[indice + 1:indice + inc]
        _replace = roman_to_int(_substr)
    text = text.replace(_substr, _replace)
    indice = text.find(' %s' % symbol)
    if indice == -1:
        return text
    return find_left(text, indice, symbol)


def find_right(text, indice, symbol):
    inc = 0
    while True:
        inc += 1
        if len(text) == indice + inc:
            break
        if text[indice - inc] not in symboles:
            break
    if len(text) != indice + inc and text[indice + 1: indice + 2] == 'e':
        _substr = text[indice - inc + 1:indice + 3]
        if _substr in ['Le ', 'Ce ']:
            return text
        _replace = roman_to_int(text[indice - inc + 1:indice + 1]) + 'ème '
    else:
        _substr = text[indice - inc + 1:indice + 1]
        if _substr in ['Le ', 'Ce ']:
            return text
        if indice - 1 == -1:
            _replace = roman_to_int(_substr)
        elif text[indice - inc] in prefix_ponctuation:
            _replace = roman_to_int(_substr)
        elif text[indice - 2:indice - 1] in prefix_space_ponctuation:
            _replace = roman_to_int(_substr)
        else:
            return text
    text = text.replace(_substr, _replace)
    indice = text.find(' %s' % symbol)
    if indice == -1:
        return text
    return find_left(text, indice, symbol)


def replace(text):
    for symbol in symboles:
        indice = text.find(' %s' % symbol)
        if indice != -1:
            text = find_left(text, indice, symbol)
            continue
        indice = text.find('%s ' % symbol)
        if indice != -1:
            text = find_right(text, indice, symbol)
            continue
        indice = text.find('%sème ' % symbol)
        if indice != -1:
            text = find_right(text, indice, symbol)
            continue
        indice = text.find('%se ' % symbol)
        if indice != -1:
            text = find_right(text, indice, symbol)
            continue
        indice = text.find('%sᵉ ' % symbol)
        if indice != -1:
            text = find_right(text, indice, symbol)
            continue
    return text
