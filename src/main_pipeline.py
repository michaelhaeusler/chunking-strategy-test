
"""Simple orchestrator demo for the starter project.
Usage:
    python src/main_pipeline.py --pdf data/sample_policy.pdf
"""
import argparse
from chunk_structure import structure_chunk
from chunk_semantic import semantic_refine
from embed_index import embed_chunks
from parse_pdf import parse_pdf



def main(pdf):
    elems = parse_pdf("../data/sample_policy.pdf")
    chunks = structure_chunk(elems)
    refined = semantic_refine(chunks)
    print(f'Produced {len(refined)} chunks. Embedding first 10...')
    idx, meta = embed_chunks(refined[:50])
    print('Index written to data/faiss_index.index and metadata file.')
    print("Detected element types:", set(el["type"] for el in elems))

if __name__ == '__main__':
    p = 'data/sample_policy.pdf'
    main(p)
