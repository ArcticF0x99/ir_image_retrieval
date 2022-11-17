import pyterrier as pt

if __name__ == '__main__':
    pt.init()
    dataset = pt.get_dataset('irds:touche-image/2022-06-13')
    # Index touche-image/2022-06-13
    indexer = pt.IterDictIndexer('./indices/touche-image_2022-06-13')
    index_ref = indexer.index(dataset.get_corpus_iter(), fields=['url', 'phash'])
