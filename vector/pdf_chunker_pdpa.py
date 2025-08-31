
import re
import os
import json
import argparse
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple

try:
    from PyPDF2 import PdfReader
except Exception as e:
    raise SystemExit(f"PyPDF2 is required to run this script. Error: {e}")

import pandas as pd


PART_PATTERNS = [
    r"(?im)^\s*Part\s+\d+[A-Z]?\s*[—-]\s*.+$",
    r"(?im)^\s*PART\s+\d+[A-Z]?\s*(:|—|-)\s*.+$",
]

SCHEDULE_PATTERNS = [
    r"(?im)^\s*(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth)\s+Schedule\s*:?.*$",
    r"(?im)^\s*SCHEDULE\s+\d+\s*:?.*$",
    r"(?im)^\s*Schedules?\s*(\(.*\))?\s*$",
]

SECTION_PATTERNS = [
    r"(?im)^\s*(Section|Sec\.?)\s+\d+[A-Z]?\s*[:—-]\s*.+$",
    r"(?im)^\s*\d+[A-Z]?\.\s+.+$",
    r"(?im)^\s*s?\d+[A-Z]?\s+.+$",
]


@dataclass
class Chunk:
    id: str
    doc_id: str
    section: str
    step: Optional[int]
    headings: List[str]
    text: str
    metadata: Dict[str, str]


def extract_pdf_text(pdf_path: str) -> List[str]:
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        pages.append(txt)
    return pages


def find_boundaries(pages: List[str], patterns: List[str]) -> List[Tuple[int, str]]:
    full_text = "\n".join(pages)
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, full_text):
            line = m.group(0).strip()
            hits.append((m.start(), line))
    hits = sorted(set(hits), key=lambda x: x[0])
    return hits


def slice_by_boundaries(full_text: str, boundaries: List[Tuple[int, str]]):
    if not boundaries:
        return [("Document", full_text)]
    result = []
    for i, (start_idx, heading) in enumerate(boundaries):
        end_idx = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(full_text)
        segment = full_text[start_idx:end_idx].strip()
        result.append((heading, segment))
    return result


def pagesize_chunks(pages: List[str], window: int = 5):
    result = []
    for i in range(0, len(pages), window):
        seg_pages = pages[i:i + window]
        result.append((f"Pages {i+1}-{i+len(seg_pages)}", "\n".join(seg_pages).strip()))
    return result


def normalize_heading(h: str) -> str:
    one_line = " ".join(h.split())
    return one_line.replace("—", "-").strip(" :")


def detect_part_boundaries(pages: List[str]):
    return find_boundaries(pages, PART_PATTERNS + SCHEDULE_PATTERNS)


def detect_section_boundaries(pages: List[str]):
    return find_boundaries(pages, SECTION_PATTERNS)


def build_chunks(
    pdf_path: str,
    doc_id: str,
    source: str,
    jurisdiction: str,
    topic: str,
    strategy: str = "part",
    page_window: int = 5,
    extra_keywords: Optional[List[str]] = None,
):
    pages = extract_pdf_text(pdf_path)
    full_text = "\n".join(pages)

    if strategy == "part":
        boundaries = detect_part_boundaries(pages)
        segments = slice_by_boundaries(full_text, boundaries)
        semantic_scope = "part-level-consolidated"
        hierarchy_base = [topic] if topic else ["Document"]
    elif strategy == "section":
        boundaries = detect_section_boundaries(pages)
        if len(boundaries) < 3:
            boundaries = detect_part_boundaries(pages)
            segments = slice_by_boundaries(full_text, boundaries)
            semantic_scope = "part-level-consolidated (fallback from section)"
        else:
            segments = slice_by_boundaries(full_text, boundaries)
            semantic_scope = "section-level"
        hierarchy_base = [topic] if topic else ["Document"]
    elif strategy == "pagesize":
        segments = pagesize_chunks(pages, window=page_window)
        semantic_scope = f"fixed-pagesize-{page_window}"
        hierarchy_base = [topic] if topic else ["Document"]
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    chunks = []
    base_keywords = ["Singapore", "data protection", "compliance", "privacy", "law", "policy"]
    if extra_keywords:
        base_keywords.extend(extra_keywords)

    for idx, (heading, text) in enumerate(segments):
        section_name = normalize_heading(heading)
        headings = [section_name] if section_name else ["Document"]
        chunk = Chunk(
            id=f"{doc_id}#{idx}",
            doc_id=doc_id,
            section=section_name,
            step=None,
            headings=headings,
            text=text,
            metadata={
                "source": source,
                "jurisdiction": jurisdiction,
                "topic": topic,
                "keywords": ", ".join(sorted(set(base_keywords))),
                "semantic_scope": semantic_scope,
                "hierarchy_path": " > ".join(hierarchy_base + [section_name or f"Chunk {idx}"]),
            },
        )
        chunks.append(chunk)
    return chunks


def write_outputs(chunks, out_dir: str, doc_id: str):
    os.makedirs(out_dir, exist_ok=True)
    jsonl_path = os.path.join(out_dir, f"{doc_id}_chunks.jsonl")
    csv_path = os.path.join(out_dir, f"{doc_id}_chunks.csv")

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for c in chunks:
            row = {
                "id": c.id,
                "doc_id": c.doc_id,
                "section": c.section,
                "step": c.step,
                "headings": c.headings,
                "text": c.text,
                "metadata": c.metadata,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\\n")

    flat_rows = []
    for c in chunks:
        r = asdict(c)
        r["metadata"] = json.dumps(r["metadata"], ensure_ascii=False)
        flat_rows.append(r)
    pd.DataFrame(flat_rows).to_csv(csv_path, index=False)
    return jsonl_path, csv_path


def main():
    parser = argparse.ArgumentParser(description="PDF Chunker (PDPA-style) for RAG pipelines.")
    parser.add_argument("--input", required=True, help="Path to PDF file")
    parser.add_argument("--doc_id", required=True, help="Doc ID/version for output rows")
    parser.add_argument("--out_dir", default=".", help="Output directory")
    parser.add_argument("--jurisdiction", default="Singapore", help="Jurisdiction metadata")
    parser.add_argument("--topic", default="", help="Topic metadata")
    parser.add_argument("--source", default="", help="Source metadata")
    parser.add_argument("--strategy", choices=["part", "section", "pagesize"], default="part", help="Chunking strategy")
    parser.add_argument("--page_window", type=int, default=5, help="For pagesize strategy")
    parser.add_argument("--keywords", nargs="*", default=[], help="Extra keywords for metadata")
    args = parser.parse_args()

    src = args.source or f"UserUpload:{os.path.abspath(args.input)}"

    chunks = build_chunks(
        pdf_path=args.input,
        doc_id=args.doc_id,
        source=src,
        jurisdiction=args.jurisdiction,
        topic=args.topic,
        strategy=args.strategy,
        page_window=args.page_window,
        extra_keywords=args.keywords,
    )
    jsonl_path, csv_path = write_outputs(chunks, args.out_dir, args.doc_id)
    print(f"Wrote:\\n  JSONL: {jsonl_path}\\n  CSV:   {csv_path}")


if __name__ == "__main__":
    main()

'''

# Part-level chunks (best first try for statutes like PDPA)
python3 pdf_chunker_pdpa.py \
  --input "/path/to/Personal Data Protection Act 2012.pdf" \
  --doc_id "pdpa_2012_pdf_2025rev" \
  --strategy part \
  --jurisdiction "Singapore" \
  --topic "Personal Data Protection Act 2012" \
  --out_dir "./chunks"

# Section-level (if headings are well-formed; auto-falls back to part-level if too sparse)
python3 pdf_chunker_pdpa.py \
  --input "./input/{file}.pdf" \
  --doc_id "mydoc_v1" \
  --strategy section

# Fixed page windows (fallback when headings are messy)
python3 pdf_chunker_pdpa.py \
  --input "./input/{file}.pdf" \
  --doc_id "mydoc_v1" \
  --strategy pagesize \
  --page_window 5

'''