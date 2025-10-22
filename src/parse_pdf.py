"""
parse_pdf.py
PDF parsing with Open-Parse (structure- and layout-aware).
Falls back to PyMuPDF text extraction if Open-Parse is unavailable.
"""
import os

def parse_pdf(pdf_path: str):
    """
    Parse a structured PDF using Open-Parse.
    Returns: list[dict] elements = [{type, text, page, bbox, ...}]
    """
    try:
        import openparse
        from openparse.processing import SemanticIngestionPipeline

        # Create a semantic ingestion pipeline (lightweight)
        pipeline = SemanticIngestionPipeline(
            min_tokens=32,
            max_tokens=2048,
        )

        parser = openparse.DocumentParser(processing_pipeline=pipeline)
        doc = parser.parse(pdf_path)
        elements = []
        for node in doc.nodes:
            elements.append({
                "type": node.node_type or "text",
                "text": node.text or "",
                "page": getattr(node, "page_number", None),
                "bbox": getattr(node, "bbox", None),
                "metadata": {
                    "block_type": node.block_type,
                    "level": node.level,
                    "id": node.id
                }
            })
        print(f"[Open-Parse] Parsed {len(elements)} elements from {pdf_path}")
        return elements
    except ImportError:
        print("[Warning] openparse not installed, falling back to PyMuPDF text extraction.")
    except Exception as e:
        print(f"[Open-Parse failed: {e}] Falling back to PyMuPDF text extraction.")

    # ---- Fallback ----
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        elements = []
        for i, page in enumerate(doc):
            text = page.get_text("text")
            elements.append({"type": "text", "text": text, "page": i + 1})
        return elements
    except Exception:
        # last resort: read as plain text
        with open(pdf_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return [{"type": "text", "text": text, "page": 1}]
