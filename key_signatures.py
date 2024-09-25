import argparse
from os import makedirs, path, environ
from glob import glob
import subprocess
import shutil
from PIL import Image
import numpy as np
import pandas as pd


KEYS = {
    'C major': 'No flats or sharps',
    'A minor': 'No flats or sharps',

    'G major': 'One sharp: F#',
    'D major': 'Two sharps: F#, C#',
    'A major': 'Three sharps: F#, C#, G#',
    'E major': 'Four sharps: F#, C#, G#, D#',
    'B major': 'Five sharps: F#, C#, G#, D#, A#',
    'F# major': 'Six sharps: F#, C#, G#, D#, A#, E#',
    'C# major': 'Seven sharps: F#, C#, G#, D#, A#, E#, B#',

    'E minor': 'One sharp F#',
    'B minor': 'Two sharps: F#, C#',
    'F# minor': 'Three sharps: F#, C#, G#',
    'C# minor': 'Four sharps: F#, C#, G#, D#',
    'G# minor': 'Five sharps: F#, C#, G#, D#, A#',
    'D# minor': 'Six sharps: F#, C#, G#, D#, A#, E#',

    'F major': 'One flat: Bb',
    'Bb major': 'Two flats: Bb, Eb',
    'Eb major': 'Three flats: Bb, Eb, Ab',
    'Ab major': 'Four flats: Bb, Eb, Ab, Db',
    'Db major': 'Five flats: Bb, Eb, Ab, Db, Gb',
    'Gb major': 'Six flats: Bb, Eb, Ab, Db, Gb, Cb',
    'Cb major': 'Seven flats: Bb, Eb, Ab, Db, Gb, Cb, Fb',

    'D minor': 'One flat: Bb',
    'G minor': 'Two flats: Bb, Eb',
    'C minor': 'Three flats: Bb, Eb, Ab',
    'F minor': 'Four flats: Bb, Eb, Ab, Db',
    'Bb minor': 'Five flats: Bb, Eb, Ab, Db, Gb',
    'Eb minor': 'Six flats: Bb, Eb, Ab, Db, Gb, Cb'
}

CLEFS = ['bass', 'treble']

KEY_TAGS = {
    'F# major': 'uncommon',
    'Gb major': 'uncommon',
    'Eb minor': 'uncommon',
    'C# major': 'rare',
    'D# minor': 'rare',
    'Cb major': 'rare'
}

# cropping parameters. for some reason vertical position is slight different between clefs
X_START = 0.1
X_WIDTH = 0.13
Y_START = {'treble': 0.018, 'bass': 0.013}
Y_WIDTH = {'treble': 0.055, 'bass': 0.05}


def key_to_lilypond_vars(key_mode_str):
    """str->(str,str), e.g. 'Eb minor'->('ees', 'minor')"""
    key, mode = key_mode_str.split()
    ly_key = key[0].lower()
    if len(key) > 1:
        if key[1] == '#':
            ly_key += 'is'
        else:
            ly_key += 'es'
    return ly_key, mode



if __name__ == '__main__':

    out_dir = 'images'


    # create lilypond files
    with open('key_signature_template.ly') as f:
        template = f.read()
    lilypond_dir = path.join(out_dir, 'lilypond')
    makedirs(lilypond_dir, exist_ok=True)

    for key_name in KEYS:
        key, mode = key_to_lilypond_vars(key_name)
        for clef in CLEFS:
            lilypond_code = template
            lilypond_code = lilypond_code.replace('##CLEF##', clef)
            lilypond_code = lilypond_code.replace('##MODE##', mode)
            lilypond_code = lilypond_code.replace('##KEY##', key)
            lilypond_fn = f'{key_name.replace(" ","_")}_{clef}.ly'
            lilypond_fn = path.join(lilypond_dir, lilypond_fn)
            with open(lilypond_fn, 'wt') as f:
                f.write(lilypond_code)

    # # convert to png
    # temp_dir = path.join(out_dir, 'full-sized-images')
    # makedirs(temp_dir, exist_ok=True)
    # lilypond_fns = sorted(glob(path.join(lilypond_dir, '*.ly')))
    # for num, lilypond_fn in enumerate(lilypond_fns):
    #     print(f'Processing {path.basename(lilypond_fn)} ({num+1} of {len(lilypond_fns)})')

    #     im_fn = path.splitext(path.basename(lilypond_fn))[0]
    #     im_fn = path.join(temp_dir, im_fn)
    #     cmd = f'lilypond --silent --png --output={im_fn} -d resolution=600 {lilypond_fn}'
    #     subprocess.check_call(cmd, shell=True, env=dict(PATH=environ['PATH']))

    #     # crop the full page to the beginning of first line
    #     im = np.array(Image.open(f'{im_fn}.png'))
    #     if 'treble' in lilypond_fn:
    #         y_width = Y_WIDTH['treble']
    #         y_start = Y_START['treble']
    #     else:
    #         y_width = Y_WIDTH['bass']
    #         y_start = Y_START['bass']
    #     xmin = int(round(X_START*im.shape[1]))
    #     xmax = xmin + int(round(X_WIDTH*im.shape[1]))
    #     ymin = int(round(y_start*im.shape[0]))
    #     ymax = ymin + int(round(y_width*im.shape[0]))
    #     crop = im.copy()[ymin:ymax, xmin:xmax]

    #     crop_fn = path.join(out_dir, path.basename(f'{im_fn}.png'))
    #     Image.fromarray(crop).save(crop_fn)

    
    rows = []
    for key_name, num_sharps_flats in KEYS.items():
        mode = key_name.split()[1]
        rows.append({
            'front': f'{num_sharps_flats}<br>{mode.capitalize()}',
            'back': key_name,
            'tag': KEY_TAGS.get(key_name, '')
        })
        rows.append({
            'front': f'Number of sharps/flats in {key_name}',
            'back': num_sharps_flats,
            'tag': KEY_TAGS.get(key_name, '')
        })
        for clef in CLEFS:
            im_fn = f'{key_name.replace(" ","_")}_{clef}.png'
            html = f'<img src="{im_fn}"><br>{mode.capitalize()}'
            rows.append({
                'front': html,
                'back': key_name,
                'tag': KEY_TAGS.get(key_name, '')
            })

    df = pd.DataFrame(rows)
    df.to_csv('key_signatures.csv', index=False, header=False)
