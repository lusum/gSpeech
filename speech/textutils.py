import codecs
import glob
import os
import re


def _replace_txt(text, line):
    bad = line.split('=')[0]
    if line.find('=') == -1:
        return text
    good = line.split('=')[1].replace('\n', '')
    return text.replace(bad, good)


def _replace_ponctuation(text, line):
    bad = line.split('=')[0]
    if line.find('=') == -1:
        return text
    good = line.split('=')[1].replace('\n', '')
    text = text.replace(bad + '.', good + '.')
    text = text.replace(bad + ';', good + ';')
    text = text.replace(bad + ',', good + ',')
    text = text.replace(bad + '?', good + '?')
    text = text.replace(bad + '!', good + '!')
    text = re.sub(bad + '$', good, text)

    text = text.replace(bad + ' ', good + ' ')
    text = re.sub(bad + ' $', good, text)
    return text


def replace(text, dict_path):
    if not os.path.isdir(dict_path):
        return text
    dict_list = glob.glob('%s/*dic' % dict_path)
    for path in sorted(dict_list):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                text = _replace_txt(text, line)

    dict_ponctuation_list = glob.glob('%s/*dic.ponctuation' % dict_path)
    for path in sorted(dict_ponctuation_list):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                text = _replace_ponctuation(text, line)
    return text


def text_to_dict(text, dict_path, lang):
    text = text.replace('\"', '')
    text = text.replace('`', '')
    text = text.replace('´', '')
    if lang != 'fr-FR':
        text = text.replace('-', '')
    text = replace(text, dict_path)
    if lang == 'fr-FR':
        from .workers.fr_FR import acronyme
        text = acronyme.too_consonnant(text)
    return text.lower()
