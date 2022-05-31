# Expression of Moral Foundations in the Polish Parliamentary Corpus

To rerun the study:

Create a virtual environment and install the requirements:

```sh
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

Download the [corpus](http://clip.ipipan.waw.pl/PPC) and unpack it into the folder `./data/raw`.

Run the Python scripts:

`1_parse_raw_data.py` - parse the corpus into text files which will be save in `./data/parsed`.

`2_lemmatize_parsed_data.py` - extract lemmas from the text files and save them into `./data/lemmatized` as JSON.

`3_compute_counts_on_lemmas` - count the number of matches for each element of MFD-PL and time period. The results are saved in `./data/couunts`.

`4_analysis.ipynb` - a Jupyter notebook to reproduce the analysis.

The folder `./data/results` contains the CSV files and timeseries plots.
# moral_foundations_dictionary_pl_polish_parliamentary_corpus
