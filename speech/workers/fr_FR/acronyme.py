import re


def _space_all_caracters(text, subtext):
    return text.replace(
        subtext,
        ' '.join(subtext[i:i + 1] for i in range(0, len(subtext), 1))
    )


def too_consonnant(text):
    pattern = r'[bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ]{4,}\b'
    for subtext in re.findall(pattern, text):
        text = _space_all_caracters(text, subtext)
    return text
