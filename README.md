# PDFOutliner – Intelligent Document Structure Extraction

## 📑 Overview
**PDFOutliner** is a Python-based tool that extracts clean, hierarchical outlines from PDF documents.  
By analyzing document structure, it generates a **navigable JSON representation** of headings (H1–H3) and their relationships, enabling **advanced navigation, search, and content analysis**.

---

## ✨ Key Features
### 🧠 Intelligent Structure Recognition
- Analyzes **font size, weight, and positioning** to detect headings  
- Identifies **hierarchical relationships** between headings  
- Preserves original **document organization**

### ⚙️ Robust Processing Engine
- Works with **inconsistently formatted** PDFs  
- Supports **multi-page** documents  
- **Language-agnostic** text analysis

### 📂 Clean, Structured Output
- **Standards-compliant JSON** output  
- Preserves heading **hierarchy**  
- Includes **page numbers** for easy navigation

---

## 🚀 Getting Started

### 📋 Prerequisites
- **Python** 3.10 or later  
- **pip** (Python package manager)  
- **Docker** *(optional, for containerized usage)*

---

### 💻 Installation (Python)
```bash
# Clone the repository
git clone https://github.com/Dhwanitisshah/Structured-PDF-Outline-Extractor.git
cd Structured-PDF-Outline-Extractor

# Install dependencies
pip install -r requirements.txt
```

---

### 🐳 Installation (Docker)
```bash
# Build the Docker image
docker build -t pdfoutliner .

# Run the container
docker run -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdfoutliner
```

---

## 📊 Usage

### Python
```bash
# Place your PDF in the input folder
mkdir -p input output
cp your_document.pdf input/

# Run the script
python pdf_outliner.py

# Output will be in the 'output' folder as JSON
```

### Docker
```bash
docker run -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdfoutliner
```

---

## 📥 Input / 📤 Output

**Input**  
- Location: `/app/input`  
- Format: PDF files (`*.pdf`)

**Output**  
- Location: `/app/output`  
- Format: JSON (same name as input PDF)  

**Example Output**
```json
{
  "title": "Sample Document",
  "headings": [
    {
      "text": "Introduction",
      "level": 1,
      "page": 1,
      "children": [
        {
          "text": "Background",
          "level": 2,
          "page": 1
        }
      ]
    }
  ]
}
```

---

## 🛠 Technical Details

**Architecture** – Hybrid approach combining:
1. **Native PDF Structure Analysis** – Extracts built-in outlines when available  
2. **Heuristic Font Analysis** – Detects headings based on font size, weight, and style  
3. **Position-Based Context** – Uses text positioning to infer hierarchy  

**Dependencies**
- **PyMuPDF** – Layout-aware text extraction  
- **pdfplumber** – Font metadata analysis  
- **Python Standard Libraries** – `re`, `collections`, `json`, `logging`

---

## 📂 Project Structure
```
Structured-PDF-Outline-Extractor/
│── input/                # PDF files to process
│── output/               # Extracted JSON outlines
│── pdf_outliner.py       # Main script
│── requirements.txt      # Python dependencies
│── Dockerfile            # Docker build configuration
│── README.md             # Project documentation
```

---

## 🔮 Future Development
- 🌐 **Enhanced Language Support** for non-Latin scripts  
- 🤖 **NLP Integration** for better heading context analysis  
- 📊 **Confidence Scoring** for extraction accuracy  
- 🌍 **Web API** for remote PDF processing  
- 📦 **Batch Processing** for multiple files

---

## 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.


