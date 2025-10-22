
"""embed_index.py
Skeleton code to embed chunks and store in FAISS.
Replace embedding call with your preferred provider (OpenAI, HuggingFace, etc.).
"""
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os, pickle

def embed_chunks(chunks, model_name='all-MiniLM-L6-v2', index_path='data/faiss_index'):
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    model = SentenceTransformer(model_name)
    texts = [c['text'] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    # store index and metadata
    faiss.write_index(index, index_path + '.index')
    with open(index_path + '.meta.pkl', 'wb') as f:
        pickle.dump(chunks, f)
    return index, chunks

def query_index(query, index_path='data/faiss_index', model_name='all-MiniLM-L6-v2', top_k=5):
    model = SentenceTransformer(model_name)
    q_emb = model.encode([query], convert_to_numpy=True)
    import faiss
    index = faiss.read_index(index_path + '.index')
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, top_k)
    with open(index_path + '.meta.pkl', 'rb') as f:
        meta = pickle.load(f)
    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(meta):
            results.append((meta[idx], float(score)))
    return results

if __name__ == '__main__':
    # quick demo (uses sample chunks)
    from src.parse_pdf import parse_pdf_basic
    from src.chunk_structure import structure_chunk
    elems = parse_pdf_basic('data/sample_policy.pdf')
    ch = structure_chunk(elems)
    idx, meta = embed_chunks(ch[:10])
    res = query_index('cancellation period for policy', top_k=3)
    print('Top results:')
    for r, s in res:
        print(s, r['heading'], r['text'][:200])
