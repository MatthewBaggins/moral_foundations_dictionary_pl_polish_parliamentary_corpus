# General
import os
import numpy as np
from dotenv import load_dotenv; load_dotenv()
from typing import Optional
from utils.json_utils import load_json, dump_json

# Timing
from codetiming import Timer
from tqdm import tqdm

# NLP
import regex as re

# Constants
MATCHES_PER_YEAR_ENOUGH_THRESHOLD = 100_000
DATA_MFD_PATH = os.getenv('DATA_MFD_PATH')
DATA_LEMMATIZED_PATH = os.getenv('DATA_LEMMATIZED_PATH')
DATA_COUNTS_PATH = os.getenv('DATA_COUNTS_PATH')

w2f: dict[str, list[str]] = load_json(f'{DATA_MFD_PATH}/w2f_pl.json') #type:ignore
    
def get_w_re(w: str) -> re.Pattern[str]:
    pat = r'\b' + w.replace('*', r'\w*') + r'\b'
    return re.compile(pat)

def load_w2re() -> dict[str, re.Pattern[str]]:
    w2re = {w: get_w_re(w) for w in sorted(w2f)}
    return w2re

def count_lemmas(re_w: re.Pattern[str], text_lemmas: str) -> int:
    return len(re_w.findall(text_lemmas))

def initialize_counts() -> dict[str, int]:
    return {w:0 for w in sorted(w2f)}# | {'total_lemmas': 0, 'total_matches': 0}

def compute_counts_sum(counter: dict[str, int]) -> int:
    return int(np.sum([counter[w] for w in w2f]))

def main() -> None:
    w2re = load_w2re()
    batches: list[tuple[str, str]] = [(f'{DATA_LEMMATIZED_PATH}/{d}', d.replace('.json', '')) for d in sorted(os.listdir(DATA_LEMMATIZED_PATH))]
    periods = sorted(dict.fromkeys([b[1].split('b')[0] for b in batches]))
    period2batches: dict[str, list[tuple[str, str]]] = {p: [b for b in batches if p in b[1]] for p in periods}
    
    start_i = 0
    end_i = None
    if end_i is None:
        end_i = len(batches)

    t = Timer()
    for i, (period_name, period_batches) in enumerate(sorted(period2batches.items())[start_i:end_i], start_i):
        t.start()
        #
        print(f'[{str(i).zfill(2)}/{len(periods)}] | Processing period {period_name} | {len(period_batches)} batch{"es" if len(period_batches) > 1 else ""}')

        counts = initialize_counts()
        total_lemmas = 0
        total_matches = 0
        for batch_path, batch_name in tqdm(period_batches):
            batch_lemmas: list[str] = load_json(batch_path) #type:ignore
            batch_lemmas_str = ' '.join(batch_lemmas)
            # print(f'Batch {batch_name} | Length: {len(batch_lemmas)} lemmas')

            for w, re_w in w2re.items():
                counts[w] += count_lemmas(re_w, batch_lemmas_str)
            total_lemmas += len(batch_lemmas)
            total_matches += compute_counts_sum(counts)
            # print(f'{total_matches = } ({100*(total_matches/MATCHES_PER_YEAR_ENOUGH_THRESHOLD):.2f} %)')
            # if total_matches > MATCHES_PER_YEAR_ENOUGH_THRESHOLD:
            #     break
            

        results = dict(period=period_name, 
                       counts=counts, 
                       total_lemmas=total_lemmas, 
                       total_matches=total_matches)
        save_path = f'{DATA_COUNTS_PATH}/{period_name}.json'
        dump_json(results, save_path)
        #
        t.stop()
    

if __name__ == '__main__':
    main()
    