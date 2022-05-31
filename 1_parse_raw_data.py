# General
import numpy as np
import os
from typing import TypeVar
from utils.file_utils import load_text_file, dump_text_file

# Timing
from codetiming import Timer

# NLP
import regex as re
re_file_content = re.compile(r'(?<!"#komentarz")>([^<]+)</u>')
def trim_content(txt: str) -> str:
    return re.sub('\n{2,}', '\n', txt).strip()

# PATH
DATA_RAW_PATH = './data/raw/ppc-nanno'
DATA_PARSED_PATH = './data/parsed'
CONTENT_LENGTH_THRESHOLD = 206745716

T = TypeVar('T')
def shuffle(xs: list[T]) -> list[T]:
    np.random.seed(42)
    inds = np.random.choice(range(len(xs)), len(xs), replace=False)
    shuffled_xs = [xs[i] for i in inds]
    return shuffled_xs

def parse_text_file(path: str) -> str:
    global re_file_content
    text = load_text_file(path)
    content = '\n'.join(re_file_content.findall(text))
    return trim_content(content)


def parse_period(path: str) -> str:
    text_file_paths = shuffle([f'{root}/text_structure.xml' 
                               for root, dirs, files in os.walk(path, topdown=False) 
                               if not dirs])
    content: str = ''
    for tf_path in text_file_paths:
        tf_parsed = parse_text_file(tf_path)
        content += tf_parsed
        if len(content) > CONTENT_LENGTH_THRESHOLD:
            break
    return content
    
def main() -> None:
    periods = [(f'{DATA_RAW_PATH}/{d}', d) for d in sorted(os.listdir(DATA_RAW_PATH)) if '.' not in d]
    t = Timer()
    start_i = 0
    end_i = None

    if end_i is None:
        end_i = len(periods)
    for i, (period_path, period_name) in enumerate(periods[start_i:end_i], 1+start_i):
        t.start()
        print(f'{str(i).zfill(2)}/{len(periods)} | Processing period {period_name}')
        
        parsed_content = parse_period(period_path)
        dump_path = f'{DATA_PARSED_PATH}/{period_name}.txt'
        dump_text_file(parsed_content, dump_path)
            
        t.stop()        
        
if __name__ == '__main__':
    main()
    
