from typing import List, Tuple
import spacy
from wordfreq import zipf_frequency

nlp = spacy.load('en_core_web_lg')

def generate_phrases(topics : List[str], method : str) -> Tuple[List[str], List[str]]:
    if method == 'frequency':
        return _generate_phrases_freq(topics)
    if method == 'naive':
        return _generate_phrases_naive(topics)
        
    
def _generate_phrases_naive(topics: List[str]) -> Tuple[List[str], List[str]]:
    positive_queries = [t for t in topics]
    negative_queries = ['not ' + t for t in topics]
    return (positive_queries, negative_queries)
    
def _generate_phrases_freq(topics: List[str]) -> Tuple[List[str], List[str]]:
    docs = list(nlp.pipe(topics))
    positive_queries = []
    negative_queries = []
    for doc in docs:
        root = str(next(doc.sents).root.lemma_)
        words = [str(x) for x in doc if zipf_frequency(str(x), 'en') < 5.6 and x.pos_ != 'PUNCT' and x.lemma_ != root]
        positive_queries.append(root + ' ' + ' '.join(words))
        negative_queries.append('not ' + root + ' ' + ' '.join(words))
    
    return (positive_queries, negative_queries)