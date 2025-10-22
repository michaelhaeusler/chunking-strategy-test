
"""structure_chunk.py
Simple structure-aware chunking skeleton.

Strategy implemented:
1) Use headings heuristics (lines with ALL CAPS or numbering like 1., 1.1, Article I)
2) Group following paragraphs until next heading
3) Ensure chunk max token approximation (by character length) and overlap
"""
import re
from typing import List, Dict

HEADING_RE = re.compile(r'^(?:ARTICLE\s+\w+|SECTION\s+\d+|\d+(?:\.\d+){0,3}\s+|[A-Z][A-Z\s]{5,})')

def is_heading(line: str) -> bool:
    if not line: return False
    line = line.strip()
    if len(line) > 5 and line.isupper():
        return True
    if HEADING_RE.match(line):
        return True
    return False

def structure_chunk(elements: List[Dict], max_chars=2500, overlap_chars=300):
    """Given elements from parse_pdf_basic, produce a list of chunks with metadata.
    Each chunk: {id, text, start_page, end_page, heading (if available), source_elements}
    """
    chunks = []
    chunk_id = 0
    for el in elements:
        # naive split by paragraphs
        paras = [p.strip() for p in el['text'].split('\n\n') if p.strip()]
        current_heading = None
        current_buf = []
        current_pages = (el.get('page',1), el.get('page',1))
        def flush_buf():
            nonlocal chunk_id, current_buf, current_heading, current_pages
            if not current_buf: return
            text = '\n\n'.join(current_buf).strip()
            chunks.append({
                'id': f'chunk-{chunk_id:06d}',
                'text': text,
                'start_page': current_pages[0],
                'end_page': current_pages[1],
                'heading': current_heading
            })
            chunk_id += 1
            # overlap handled at caller (or could duplicate last N chars here)
            current_buf = []

        for p in paras:
            if is_heading(p):
                # heading found: flush previous
                flush_buf()
                current_heading = p.strip()
                continue
            # append paragraph
            current_buf.append(p)
            # flush if size exceeded
            if sum(len(x) for x in current_buf) > max_chars:
                flush_buf()

        # flush leftover after element
        flush_buf()

    # Optionally add overlaps (simple duplication of last N chars to next)
    if overlap_chars > 0 and len(chunks) > 1:
        for i in range(1, len(chunks)):
            prior = chunks[i-1]['text']
            overlap = prior[-overlap_chars:]
            chunks[i]['text'] = overlap + '\n\n' + chunks[i]['text']
    return chunks

if __name__ == '__main__':
    from src.parse_pdf import parse_pdf_basic
    elems = parse_pdf_basic('data/sample_policy.pdf')
    ch = structure_chunk(elems)
    print('Produced', len(ch), 'chunks. First chunk preview:\n', ch[0]['text'][:400])
