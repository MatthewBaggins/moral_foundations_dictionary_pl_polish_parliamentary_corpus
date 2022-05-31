# General
from codetiming import Timer
import os

from tqdm import tqdm

from utils.file_utils import load_text_file
from utils.json_utils import dump_json

# NLP
import morfeusz2

# Constants
DATA_PARSED_PATH = './data/parsed'
DATA_LEMMATIZED_PATH = './data/lemmatized'
MAX_BATCH_LENGTH = 10_000_000

morf = morfeusz2.Morfeusz()
def get_batch_lemmas(batch: str) -> list[str]:
    global morf, MAX_BATCH_LENGTH
    indexed_lemmas: list[tuple[int, str]] = []
    batch_analysed = morf.analyse(batch)
    indexed_lemmas.extend(list(dict.fromkeys(((a[0], 
                                               a[2][1].split(':')[0].lower())
                                              for a in batch_analysed))))
    lemmas = [il[1] for il in indexed_lemmas if il[1].isalpha()]
    return lemmas

def main() -> None:
    parsed_fnames = sorted(os.listdir(DATA_PARSED_PATH))

    t = Timer()

    # Settings
    start_i = 0
    end_i = None
    if end_i is None:
        end_i = len(parsed_fnames)

    for i, fname in enumerate(parsed_fnames[start_i:end_i], start_i+1):
        t.start()
        #
        period_name = fname.replace('.txt', '')
        text = load_text_file(f'{DATA_PARSED_PATH}/{fname}')
        batch_inds = [(i*MAX_BATCH_LENGTH, (i+1)*MAX_BATCH_LENGTH) for i in range((len(text) // MAX_BATCH_LENGTH) + 1)]
        print(f'[{str(i).zfill(2)}/{len(parsed_fnames)}] | Processing period {period_name} | Length: {len(text)} characters; {len(batch_inds)} batch{ "es" if len(batch_inds)>1 else "" }')
        if len(batch_inds) > 1:
            print(f'{len(batch_inds)} batches')
        for b_i, (batch_i0, batch_i1) in tqdm(enumerate(batch_inds), disable=len(batch_inds)==1):
            batch_lemmas = get_batch_lemmas(text[batch_i0 : batch_i1])
            batch_lemmas_path = f'{DATA_LEMMATIZED_PATH}/{period_name}b{b_i}.json'
            dump_json(batch_lemmas, batch_lemmas_path)
        #
        t.stop()    
        
    

if __name__ == '__main__':
    main()
    