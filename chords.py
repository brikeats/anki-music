from os import path, makedirs
import pandas as pd


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

out_dir = 'chord_lilypond_files'
makedirs(out_dir, exist_ok=True)


for _, row in chords_df.iterrows():
    chord_name = row['Chord']
    for inv_num, inv_name in enumerate(INVERSIONS):
        note_0 = row[f'Note_{inv_num}']
        note_1 = row[f'Note_{(inv_num+1)%len(INVERSIONS)}']
        note_2 = row[f'Note_{(inv_num+2)%len(INVERSIONS)}']
        closed_notes = [note_0, note_1, note_2]
        # open_notes = [note_0, note_2, note_1]  # open

        # raise octave with single apostrophe '\''
        # lower octave with comma ','
        lilypond_notes = [n.replace('#','is').replace('b','es').lower() for n in closed_notes]
        lilypond_note_str = f'<<{" ".join(lilypond_notes)}>>'
        lilypond_code = template.replace('##NOTES##', lilypond_note_str)
        lilypond_code = lilypond_code.replace('##CLEF##', 'treble')

        filename = f'{chord_name.replace(" ", "-")}_{inv_name.replace(" ", "-")}.ly'
        filename = path.join(out_dir, filename)
        with open(filename, 'wt') as f:
            f.write(lilypond_code)


    break