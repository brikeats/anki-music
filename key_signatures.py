import argparse
from os import makedirs, path, environ
from glob import glob
import subprocess
import shutil
from PIL import Image
import numpy as np


CLEFS = [
    'treble',
    # 'alto',
    # 'tenor',
    'bass'
]

KEYS = {
    'C major': ('c', 'major'),
    'G major': ('g', 'major'),
    'D major': ('d', 'major'),
    'A major': ('a', 'major'),
    'E major': ('e', 'major'),
    'B major': ('b', 'major'),
    'F# major': ('fis', 'major'),
    'C# major': ('cis', 'major'),
    'A minor': ('a', 'minor'),
    'E minor': ('e', 'minor'),
    'B minor': ('b', 'minor'),
    'F# minor': ('fis', 'minor'),
    'C# minor': ('cis', 'minor'),
    'G# minor': ('gis', 'minor'),
    'D# minor': ('dis', 'minor'),
    'F major': ('f', 'major'),
    'Bb major': ('bes', 'major'),
    'Eb major': ('ees', 'major'),
    'Ab major': ('aes', 'major'),
    'Db major': ('des', 'major'),
    'Gb major': ('ges', 'major'),
    'Cb major': ('ces', 'major'),
    'D minor': ('d', 'minor'),
    'G minor': ('g', 'minor'),
    'C minor': ('c', 'minor'),
    'F minor': ('f', 'minor'),
    'Bb minor': ('bes', 'minor'),
    'Eb minor': ('ees', 'minor'),
}

# cropping parameters. for some reason vertical position is slight different between clefs
X_START = 0.1
X_WIDTH = 0.13
Y_START = {'treble': 0.018, 'bass': 0.013}
Y_WIDTH = {'treble': 0.055, 'bass': 0.05}


if __name__ == '__main__':

    out_dir = 'images'


    # create lilypond files
    with open('template.ly') as f:
        template = f.read()
    lilypond_dir = path.join(out_dir, 'lilypond')
    makedirs(lilypond_dir, exist_ok=True)

    for name, (key, mode) in KEYS.items():
        for clef in CLEFS:
            lilypond_code = template
            lilypond_code = lilypond_code.replace('##CLEF##', clef)
            lilypond_code = lilypond_code.replace('##MODE##', mode)
            lilypond_code = lilypond_code.replace('##KEY##', key)
            lilypond_fn = f'{name.replace(" ","_")}_{clef}.ly'
            lilypond_fn = path.join(lilypond_dir, lilypond_fn)
            with open(lilypond_fn, 'wt') as f:
                f.write(lilypond_code)

    # convert to png
    temp_dir = path.join(out_dir, 'full-sized-images')
    makedirs(temp_dir, exist_ok=True)
    lilypond_fns = sorted(glob(path.join(lilypond_dir, '*.ly')))
    for num, lilypond_fn in enumerate(lilypond_fns):
        print(f'Processing {path.basename(lilypond_fn)} ({num+1} of {len(lilypond_fns)})')

        im_fn = path.splitext(path.basename(lilypond_fn))[0]
        im_fn = path.join(temp_dir, im_fn)
        cmd = f'lilypond --silent --png --output={im_fn} -d resolution=600 {lilypond_fn}'
        subprocess.check_call(cmd, shell=True, env=dict(PATH=environ['PATH']))

        # crop the full page to the beginning of first line
        im = np.array(Image.open(f'{im_fn}.png'))
        if 'treble' in lilypond_fn:
            y_width = Y_WIDTH['treble']
            y_start = Y_START['treble']
        else:
            y_width = Y_WIDTH['bass']
            y_start = Y_START['bass']
        xmin = int(round(X_START*im.shape[1]))
        xmax = xmin + int(round(X_WIDTH*im.shape[1]))
        ymin = int(round(y_start*im.shape[0]))
        ymax = ymin + int(round(y_width*im.shape[0]))
        crop = im.copy()[ymin:ymax, xmin:xmax]

        crop_fn = path.join(out_dir, path.basename(f'{im_fn}.png'))
        Image.fromarray(crop).save(crop_fn)
