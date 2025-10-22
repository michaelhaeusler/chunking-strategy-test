
# Notebook-style script: 01_chunking_experiments.py
# Use this to interactively try different chunking strategies.

from src.parse_pdf import parse_pdf_basic
from src.chunk_structure import structure_chunk, is_heading
from src.chunk_semantic import semantic_refine

elems = parse_pdf_basic('data/sample_policy.pdf')
chunks = structure_chunk(elems, max_chars=1500, overlap_chars=200)
print('Chunks:', len(chunks))
for i,c in enumerate(chunks[:5]):
    print('\n--- CHUNK', i, 'HEADING:', c.get('heading'))
    print(c['text'][:500])
refined = semantic_refine(chunks, threshold=0.84)
print('\nAfter semantic refine:', len(refined))
