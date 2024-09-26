from glob import glob
from os import path, makedirs, environ
import subprocess
import pandas as pd
from skimage import io
from tqdm import tqdm


INVERSIONS = [
    'root position',
    'first inversion',
    'second inversion'
]

VOICINGS = [
    'open',
    'closed'
]

chords_df = pd.read_csv('chord_notes.csv')

with open('chord_template.ly') as f:
    template = f.read()

out_dir = 'temp'

lilypond_dir = path.join(out_dir, 'chord_lilypond_files')
makedirs(lilypond_dir, exist_ok=True)

temp_im_dir = path.join(out_dir, 'temp_images')
makedirs(temp_im_dir, exist_ok=True)

out_im_dir = path.join(out_dir, 'images')
makedirs(out_im_dir, exist_ok=True)


print('Creating lilypond code')
for _, row in tqdm(chords_df.iterrows(), total=len(chords_df)):
    chord_name = row['Chord']
    for inv_num, inv_name in enumerate(INVERSIONS):
        note_0 = row[f'Note_{inv_num}']
        note_1 = row[f'Note_{(inv_num+1)%len(INVERSIONS)}']
        note_2 = row[f'Note_{(inv_num+2)%len(INVERSIONS)}']
        closed_notes = [note_0, note_1, note_2]
        # open_notes = [note_0, note_2, note_1]  # open

        # raise octave with single apostrophe '\''
        # lower octave with comma ','

        
        suffixes = ["", "'", "''", "'''"]
        for suffix_num, suffix in enumerate(suffixes):

            lilypond_notes = [n.replace('#','is').replace('b','es').lower() for n in closed_notes]
            lilypond_notes[0] += suffix
            lilypond_note_str = f'\\relative <<{" ".join(lilypond_notes)}>>'

            lilypond_code = template.replace('##NOTES##', lilypond_note_str)
            lilypond_code = lilypond_code.replace('##CLEF##', 'treble')

            ly_filename = f'{chord_name.replace(" ", "-")}_{inv_name.replace(" ", "-")}_{suffix_num}.ly'
            ly_filename = path.join(lilypond_dir, ly_filename)
            with open(ly_filename, 'wt') as f:
                f.write(lilypond_code)

    break


# render lilypond files
print('Rendering')
ly_filenames = sorted(glob(path.join(lilypond_dir, '*.ly')))
for ly_filename in tqdm(ly_filenames):
    png_filename = path.splitext(path.basename(ly_filename))[0]
    png_filename = path.join(temp_im_dir, png_filename)
    cmd = f'lilypond --silent --png --output={png_filename} -d resolution=600 {ly_filename}'
    subprocess.check_call(cmd, shell=True, env=dict(PATH=environ['PATH']))

# crop full page lilypond output images
ista = 100
iend = 700
jsta = 500
jend = 1050
big_png_fns = sorted(glob(path.join(temp_im_dir, '*.png')))
print('Cropping')
for big_png_fn in tqdm(big_png_fns):
    im = io.imread(big_png_fn)
    cropped_im = im[ista:iend, jsta:jend]
    cropped_png_fn = path.join(out_im_dir, path.basename(big_png_fn))
    io.imsave(cropped_png_fn, cropped_im)
