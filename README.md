# Adobe India Hackathon 2025 – Round 1A Submission  

**Challenge**: Connecting the Dots – Structured PDF Outline Extraction  
**Team**: QWERTY Coders  

## Problem Statement  
The goal is to extract a clean, hierarchical outline (Title, H1, H2, H3) from raw PDF documents, capturing structure and page numbers. This structured output lays the foundation for advanced semantic applications such as smart navigation, search, and summarization.

## Solution Overview  
Our approach analyzes PDF layout features to generate a hierarchical outline. The solution extracts:  
• Document title  
• Headings categorized as H1, H2, or H3  
• Associated page numbers and position-based context  

We use a hybrid heuristic model considering:  
• Font size and weight  
• Text position on page  
• Font type and structure layout  
This ensures robustness even when documents lack consistent formatting.

## Tech Stack  
• Language: Python 3.10  
• Libraries Used:  
   - PyMuPDF (for layout-aware text extraction)  
   - pdfplumber (for font metadata)  
   - Standard Python libraries: re, collections, json, logging

## Docker Instructions**Build the Docker Image:**  
```bash
docker build --platform linux/amd64 -t outline-extractor:<your_tag> .
```
**Run the Docker Container:**
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  outline-extractor:<your_tag>
```
## Input/Output Format

### Input
- Directory: `/app/input`
- Format: PDF files (*.pdf)
- Limit: Up to 50 pages per PDF

### Output
- Directory: `/app/output`
- Format: JSON files with same name as input PDF
- Structure:
```json

{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## Key Features

- Heuristic-based heading classification
- Language-agnostic font and layout analysis
- Accurate multi-page document parsing
- Clean, standards-compliant JSON output
- Resilient to inconsistencies in document structure

  ## Folder Structure

Adobe1A-main/
├── README.md              → Project overview and guide

├── dockerfile             → Build instructions

├── requirements.txt       → Python dependencies

├── app/
│   ├── extract_outline.py → Core extraction logic
│   ├── input/             → PDF files to be processed
│   │   └── file02.pdf

│── output/            → Extracted JSON outlines
│       └── file02.json


## Future Enhancements

- Add multilingual document support (e.g., Japanese, Devanagari)
- Integrate lightweight NLP techniques for improved heading context
- Implement confidence scoring for heading hierarchy classification

## Team
QWERTY Coders
Dhwanit Shah,Suyash Pandey,Atishay Jain
Bharati Vidyapeeth (DU) College of Engineering,Pune

## License & Confidentiality

This document is a part of the Adobe India Hackathon 2025. 
