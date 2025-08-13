"""
PDFOutliner: Intelligent PDF Structure Extraction
A tool for extracting hierarchical outlines from PDF documents
"""

import os
import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter, defaultdict
import re

import pymupdf  # PyMuPDF
import pdfplumber  # PDF font analysis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFOutlineExtractor:
    def __init__(self):
        self.font_size_threshold = 2.0
        self.min_heading_chars = 3
        self.max_heading_chars = 200

    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        logger.info(f"Processing PDF: {pdf_path}")
        start = time.time()
        
        try:
            outline = self._extract_pymupdf_outline(pdf_path)
            if not outline["outline"]:
                logger.info("No outline found, switching to font-based extraction")
                outline = self._extract_font_based_outline(pdf_path)
            if not outline["title"]:
                outline["title"] = self._extract_title(pdf_path)

            logger.info(f"Completed in {time.time() - start:.2f}s")
            return outline
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")
            return {"title": "", "outline": []}

    def _extract_pymupdf_outline(self, pdf_path: str) -> Dict[str, Any]:
        try:
            doc = pymupdf.open(pdf_path)
            toc = doc.get_toc()
            title = self._clean_title_text(doc.metadata.get('title', ''))
            doc.close()

            outline = [
                {"level": f"H{level}", "text": self._clean_heading_text(text), "page": page}
                for level, text, page in toc if level <= 3 and self._clean_heading_text(text)
            ]

            logger.info(f"PyMuPDF found {len(outline)} items")
            return {"title": title, "outline": outline}

        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}")
            return {"title": "", "outline": []}

    def _extract_font_based_outline(self, pdf_path: str) -> Dict[str, Any]:
        try:
            outline, title = [], ""
            with pdfplumber.open(pdf_path) as pdf:
                font_stats = self._analyze_font_statistics(pdf)
                heading_fonts = self._identify_heading_fonts(font_stats)
                logger.info(f"Detected heading font sizes: {list(heading_fonts.keys())}")

                for idx, page in enumerate(pdf.pages, 1):
                    outline.extend(self._extract_page_headings(page, heading_fonts, idx))

                if pdf.pages:
                    title = self._extract_title_from_page(pdf.pages[0])

            outline.sort(key=lambda x: (x["page"], x["y_position"]))
            logger.info(f"Font-based analysis found {len(outline)} headings")
            return {"title": title, "outline": outline}

        except Exception as e:
            logger.error(f"Font-based extraction failed: {e}")
            return {"title": "", "outline": []}

    def _analyze_font_statistics(self, pdf) -> Dict[float, Dict]:
        stats = defaultdict(lambda: {"count": 0, "is_bold": False, "sample": "", "positions": []})
        total = 0
        
        for page in pdf.pages:
            for c in page.chars:
                size = round(c['size'], 1)
                font = c.get('fontname', '')
                stats[size]['count'] += 1
                stats[size]['is_bold'] |= 'bold' in font.lower()
                if len(stats[size]['sample']) < 50:
                    stats[size]['sample'] += c['text']
                stats[size]['positions'].append(c['top'])
                total += 1

        for s in stats:
            stats[s]['frequency'] = stats[s]['count'] / total if total else 0

        return stats

    def _identify_heading_fonts(self, stats: Dict[float, Dict]) -> Dict[float, str]:
        if not stats:
            return {}

        body_size = max(stats, key=lambda s: stats[s]['frequency'])
        headings = {}
        level = 1

        for size in sorted(stats, reverse=True):
            stat = stats[size]
            if (size > body_size + self.font_size_threshold and 0.001 < stat['frequency'] < 0.1 and level <= 3):
                headings[size] = f"H{level}"
                level += 1

        return headings

    def _extract_page_headings(self, page, heading_fonts, page_num: int) -> List[Dict]:
        lines = self._group_by_line(page.chars)
        headings = []

        for line in lines:
            text = ''.join(c['text'] for c in line).strip()
            if not (self.min_heading_chars <= len(text) <= self.max_heading_chars):
                continue

            sizes = [round(c['size'], 1) for c in line]
            primary_size = Counter(sizes).most_common(1)[0][0]
            if primary_size in heading_fonts:
                headings.append({
                    "level": heading_fonts[primary_size],
                    "text": self._clean_heading_text(text),
                    "page": page_num,
                    "y_position": min(c['top'] for c in line),
                    "font_size": primary_size
                })

        return headings

    def _group_by_line(self, chars) -> List[List[Dict]]:
        if not chars:
            return []

        chars = sorted(chars, key=lambda c: (c['top'], c['x0']))
        lines, current, current_y = [], [chars[0]], chars[0]['top']

        for c in chars[1:]:
            if abs(c['top'] - current_y) < 5:
                current.append(c)
            else:
                lines.append(current)
                current = [c]
                current_y = c['top']

        lines.append(current)
        return lines

    def _extract_title(self, pdf_path: str) -> str:
        try:
            with pymupdf.open(pdf_path) as doc:
                title = doc.metadata.get('title', '')
                if title:
                    return self._clean_title_text(title)
            with pdfplumber.open(pdf_path) as pdf:
                return self._extract_title_from_page(pdf.pages[0]) if pdf.pages else ""
        except Exception as e:
            logger.warning(f"Title extraction failed: {e}")
            return ""

    def _extract_title_from_page(self, page) -> str:
        try:
            lines = self._group_by_line(page.chars)[:10]
            page_h, page_w = page.height, page.width
            candidates = []

            for line in lines:
                text = ''.join(c['text'] for c in line).strip()
                if not (self.min_heading_chars <= len(text) <= self.max_heading_chars):
                    continue

                size = sum(c['size'] for c in line) / len(line)
                y = min(c['top'] for c in line)
                x_center = (min(c['x0'] for c in line) + max(c['x1'] for c in line)) / 2

                score = (size/12)*0.4 + ((page_h - y)/page_h)*0.3 + (1 - abs(x_center - page_w/2)/(page_w/2))*0.3
                candidates.append((text, score))

            return self._clean_title_text(max(candidates, key=lambda x: x[1])[0]) if candidates else ""
        except Exception as e:
            logger.warning(f"Page title detection failed: {e}")
            return ""

    def _clean_heading_text(self, text: str) -> str:
        text = ' '.join(text.split())
        text = re.sub(r'^(Chapter|Section|Part)\s*\d*\.?\s*', '', text, flags=re.IGNORECASE)
        return re.sub(r'\s+\d+\s*$', '', text) if self.min_heading_chars <= len(text) <= self.max_heading_chars else ""

    def _clean_title_text(self, text: str) -> str:
        return re.sub(r'\.(pdf|docx?)$', '', ' '.join(text.split()), flags=re.IGNORECASE)[:200]


def process_pdfs():
    base = Path(__file__).resolve().parent
    input_dir, output_dir = base / "input", base / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        logger.error(f"Input dir not found: {input_dir}")
        return

    pdfs = list(input_dir.glob("*.pdf"))
    if not pdfs:
        logger.warning("No PDFs found")
        return

    extractor = PDFOutlineExtractor()
    for pdf in pdfs:
        try:
            logger.info(f"Processing {pdf.name}")
            result = extractor.extract_outline(str(pdf))
            with open(output_dir / f"{pdf.stem}.json", 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error on {pdf.name}: {e}")
            with open(output_dir / f"{pdf.stem}.json", 'w', encoding='utf-8') as f:
                json.dump({"title": "", "outline": []}, f, indent=2)


if __name__ == "__main__":
    logger.info("Starting optimized PDF outline extraction")
    process_pdfs()
    logger.info("All files processed")
