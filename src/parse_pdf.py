
"""parse_pdf.py
Minimal PDF parsing helpers (skeleton). Replace or extend with Unstructured/Open-Parse/Docling.
"""
import os

def parse_pdf_basic(pdf_path):
    """Very small placeholder parser that attempts to extract text using PyMuPDF if available,
    otherwise returns a fallback simple text element list. Replace with 'unstructured.partition' or Open-Parse in production.
    Returns: list of elements where element = {type: 'text'|'table'|'image', 'text': str, 'page': int}
    """
    elements = []
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            text = page.get_text("text")
            elements.append({"type": "text", "text": text, "page": i+1})
    except Exception as e:
        # Fallback: read as plain text file (useful in this starter project)
        if os.path.exists(pdf_path):
            with open(pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            elements.append({"type": "text", "text": text, "page": 1})
        else:
            raise RuntimeError(f"PDF path not found: {pdf_path}") from e
    return elements

if __name__ == '__main__':
    import sys
    p = sys.argv[1] if len(sys.argv) > 1 else 'data/sample_policy.pdf'
    elems = parse_pdf_basic(p)
    print(f"Parsed {len(elems)} elements. Sample:\n", elems[0]['text'][:500])
