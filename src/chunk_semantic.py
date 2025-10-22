
"""semantic_refine.py
A lightweight semantic sub-chunking using sentence-transformers.
Splits a chunk when adjacent paragraph embeddings show a topic shift (low similarity).
"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = None

def _get_model(name='all-MiniLM-L6-v2'):
    global model
    if model is None:
        model = SentenceTransformer(name)
    return model

def semantic_refine(chunks, threshold=0.82, min_paras=2):
    refined = []
    s_model = _get_model()
    for c in chunks:
        paras = [p for p in c['text'].split('\n\n') if p.strip()]
        if len(paras) <= min_paras:
            refined.append(c)
            continue
        embeds = s_model.encode(paras, show_progress_bar=False)
        # detect splits where similarity drops between adjacent paras
        split_indices = [0]
        for i in range(1, len(paras)):
            sim = cosine_similarity([embeds[i-1]], [embeds[i]])[0][0]
            if sim < threshold:
                split_indices.append(i)
        split_indices.append(len(paras))
        # create subchunks
        for i in range(len(split_indices)-1):
            sub = '\n\n'.join(paras[split_indices[i]:split_indices[i+1]])
            newc = c.copy()
            newc['text'] = sub
            refined.append(newc)
    return refined

if __name__ == '__main__':
    import json
    from src.parse_pdf import parse_pdf_basic
    from src.chunk_structure import structure_chunk
    elems = parse_pdf_basic('data/sample_policy.pdf')
    ch = structure_chunk(elems)
    refined = semantic_refine(ch[:3])
    print('Refined into', len(refined), 'subchunks')
