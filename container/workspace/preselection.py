from tira_utils import get_input_directory_and_output_directory, normalize_run
import pyterrier as pt
import pandas as pd
import os
import json
from tqdm import tqdm
from glob import glob
from pathlib import Path
from typing import List, Tuple
import shutil

SYSTEM_NAME = os.environ.get('TIRA_SYSTEM_NAME' ,'my-retrieval-system')

YEAR = 23

if not pt.started():
    # tira_utils above should already have done started pyterrier with this configuration to ensure that no internet connection is required (for reproducibility)
    pt.init(version=os.environ['PYTERRIER_VERSION'], helper_version=os.environ['PYTERRIER_HELPER_VERSION'], no_download=True)

input_directory, output_directory = get_input_directory_and_output_directory(default_input=f'/workspace/dataset{YEAR}/')

def __load_image_text(image_id):
    ret = ''
    
    for txt_file in glob(input_directory +'/images/' + image_id[:3] + '/' + image_id + '/*/*/*/text.txt'):
        ret += '\n\n' + open(txt_file).read()
        
    return ret.strip()

def __all_images():
    for i in glob(input_directory + '/images/*/*'):
        image_id = i.split('/')[-1]
        yield {'docno': image_id, 'text': __load_image_text(image_id)}

if os.path.exists(f"./index{YEAR}"):
    retrieval_pipeline = pt.BatchRetrieve(f"./index{YEAR}", wmodel="BM25", verbose=True, num_results=50)
else:
    iter_indexer = pt.IterDictIndexer(f"./index{YEAR}", meta={'docno': 27, 'text': 4096})
    index_ref = iter_indexer.index(tqdm(__all_images()))
    retrieval_pipeline = pt.BatchRetrieve(index_ref, wmodel="BM25", verbose=True, num_results=50)

def retrieve(queries : List[Tuple[str, int]]) -> pd.DataFrame:
    queries = pd.DataFrame(queries, columns=['query', 'qid'])
    return retrieval_pipeline(queries)
