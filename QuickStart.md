
# OCR Forge CLI Quickstart Guide

## What is OCR Forge CLI?

OCR Forge CLI is a powerful command-line tool that captures text from your screen, processes it with AI, and allows you to interact with the extracted content. It combines screen capture, OCR (Optical Character Recognition), and LLM (Large Language Model) processing to make working with on-screen text effortless.

## Getting Started in 5 Minutes

### 1. Prerequisites

- Python 3.6+
- Tesseract OCR installed
- Groq API key (sign up at [groq.com](https://groq.com))

### 2. Installation

```bash
# Install required Python packages
pip install mss pillow pytesseract keyboard plyer requests groq rich

# Set your Groq API key
export GROQ_API_KEY="your_groq_api_key_here"  # Linux/macOS
# or
set GROQ_API_KEY=your_groq_api_key_here       # Windows CMD
# or
$env:GROQ_API_KEY="your_groq_api_key_here"    # Windows PowerShell

# Make sure Tesseract path is correctly set in the script
# Default: pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
```

### 3. Launch OCR Forge CLI

```bash
python ocrforge.py
```

### 4. Basic Commands

- **Capture Screen Region**: Press `Ctrl + Print Screen`
- **Exit Application**: Press `Esc`
- **View History**: Run `python ocrforge.py --history`

### 5. Workflow

1. **Capture**: Press `Ctrl + Print Screen` and select a region
2. **Wait**: The tool will extract text and clean it with AI
3. **Review**: See the cleaned text in your terminal
4. **Ask Questions**: Type follow-up questions when prompted
5. **Exit Questions**: Type `exit` to stop the Q&A session

## Example Use Cases

- Extract and summarize text from articles
- Capture code snippets from videos or websites
- Extract data from charts or tables
- Capture and clean up text from PDFs displayed on screen
- Extract information from application interfaces

## Tips

- Select regions with clear, readable text for best results
- For code, the tool will automatically apply syntax highlighting
- Your capture history is saved to `history_log.json`. Please create it locally.
- Ask follow-up questions to get explanations or summaries

## Troubleshooting

- If no text is detected, try selecting a clearer region
- Ensure your Groq API key is valid and properly set
- Check that Tesseract is correctly installed and configured

For more detailed information, refer to the full documentation.