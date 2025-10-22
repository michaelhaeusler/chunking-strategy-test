
# Notebook-style script: 02_retrieval_eval.py
from src.embed_index import embed_chunks, query_index
from src.parse_pdf import parse_pdf_basic
from src.chunk_structure import structure_chunk

elems = parse_pdf_basic('data/sample_policy.pdf')
chunks = structure_chunk(elems)
idx, meta = embed_chunks(chunks[:60])
q = 'What is the cancellation notice period?'
results = query_index(q, top_k=5)
for r, score in results:
    print('SCORE', score, 'HEADING', r.get('heading'))
    print(r['text'][:400])
