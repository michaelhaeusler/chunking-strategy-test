
# Simple evaluation harness
# Measures whether a set of queries retrieve expected chunks (manual labels required).
import json, os
from src.parse_pdf import parse_pdf_basic
from src.chunk_structure import structure_chunk
from src.embed_index import embed_chunks, query_index

# Example evaluation dataset (replace with your own labeled pairs)
EVAL = [
    {'query': 'What is the cancellation notice period?', 'expected_heading_contains': 'CANCELLATION'},
    {'query': 'Who is defined as the Insured?', 'expected_heading_contains': 'DEFINITIONS'}
]

def run_eval(pdf_path='data/sample_policy.pdf'):
    elems = parse_pdf_basic(pdf_path)
    chunks = structure_chunk(elems)
    idx, meta = embed_chunks(chunks[:100])
    for q in EVAL:
        results = query_index(q['query'], top_k=3)
        print('\nQuery:', q['query'])
        for r, score in results:
            ok = q['expected_heading_contains'].lower() in (r.get('heading') or '').lower()
            print('  score:', score, 'heading:', r.get('heading'), 'match:', ok)
if __name__ == '__main__':
    run_eval()
