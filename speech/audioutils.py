import multiprocessing
import os
import subprocess

from .i18n import _text_to_long


def effect(text, speed=100, pitch=100, volume=120):
    _speed = '<speed level="%s">%s</speed>' % (speed, text)
    _pitch = '<pitch level="%s">%s</pitch>' % (pitch, _speed)
    return '<volume level="%s">%s</volume>' % (volume, _pitch)


def get_audio_commands(text, outfile, lang, cache_path, speed):
    cmds = []
    names = []
    if len(text) <= 32768:
        stream = """pico2wave -l %s -w %s '%s'""" % (
            lang,
            outfile,
            effect(text, speed * 100)
        )
        cmds.append(stream)
        names.append(outfile)
        return names, cmds
    discours = text.split('.')
    text = ''
    for idx, paragraph in enumerate(discours):
        text += paragraph
        if (
            idx == len(discours) - 1
            or len(text) + len(discours[idx + 1]) >= 32767
        ):
            filename = cache_path + 'speech' + str(idx) + '.wav'
            cmds.append(
                """pico2wave -l %s -w %s '%s'""" % (
                    lang, filename, effect(text, speed * 100)
                )
            )
            names.append(filename)
            text = ''
    return names, cmds


def run_audio_files(names, cmds, outfile):
    if len(cmds) == 1:
        os.system(cmds[0])
        return
    p = subprocess.Popen(
        ['which', 'sox'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    path, _ = p.communicate()
    if not os.path.isfile(path):
        print(_text_to_long)
        return
    nproc = int(.5 * multiprocessing.cpu_count())
    if nproc == 0:
        nproc = 1
    multiprocessing.Pool(nproc).map(os.system, cmds)
    os.system('sox %s %s' % (' '.join(names), 'out.wav'))
    for _file in names:
        os.remove(_file)
