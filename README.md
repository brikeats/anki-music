# Anki Cards for Learning Music

Generate media for use in Anki flash cards for learning to read music, and for ear training.


## Usage

Apparently, you need to use Anki Desktop to import CSVs; Ankiweb doesn't do it.

* Create an Ankiweb account
* [Install Anki Desktop](https://apps.ankiweb.net/). Click sync button and enter Ankiweb credentials
* You'll probably want to use the phone app for actual study. Install it, click the sync button and enter Ankiweb credentials

### Import CSVs

Anki can import data in CSV format. I prepared `relative-keys.csv` manually; some of the other CSVs can be created via Python scripts as described in the next section.

Once you have a CSV, import it into Anki like so:

* Open Anki Desktop
* "Create Deck", name it "Relative Keys"
* Click "Import File" and select the CSV
* In the import dialog, under "Import Options > Deck", select "Relative Keys"
* Click "Import". Close the import dialog.
* Click "Sync" to add it to your Ankiweb account

### Generate CSVs

* [Install Lillypond](https://lilypond.org/download.html). The scripts assume the `lilypond` binary is in your `PATH`.
* Create python environment: `conda create -n anki python=3 -y && conda activate anki`
* Install dependencies: `pip install requirements.txt`
* Create images of key signatures: `python key_signatures.py`

----

Media: 

Images/mp3s should go in `/Users/brian/Library/Application Support/Anki2/User 1/collection.media`. The image
`/Users/brian/Library/Application Support/Anki2/User 1/collection.media/file0001.jpg` can be referenced in CSV by `<img src="file0001.jpg">`. It seems that subfolders are not allowed; media must be directly in `collections.media` folder.

