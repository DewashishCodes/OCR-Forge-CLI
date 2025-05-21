# OCR Forge CLI Documentation 🚀

## Overview 🔍

OCR Forge CLI is a powerful screen capture and text extraction tool that combines Optical Character Recognition (OCR) with Large Language Model (LLM) processing. Created by Dewashish Lambore, this Python-based utility allows users to capture screen regions, extract text using Tesseract OCR, and then enhance the results using Groq's LLM capabilities to provide cleaner, more usable text output.

## Features ✨

- **Region-based Screen Capture** 📱: Select specific areas of your screen for targeted text extraction
- **Full Screen Capture** 🖥️: Capture and process the entire screen
- **LLM-Enhanced Text Cleaning** 🧠: Automatically improve OCR results using Groq's LLM
- **Interactive Follow-up Questions** 💬: Ask questions about the captured text
- **History Logging** 📚: Save and review past captures
- **Code Highlighting** 🔆: Properly format and display code blocks in the output
- **Hotkey Integration** ⌨️: Quick activation with keyboard shortcuts

## Requirements 📋

- Python 3.6+
- Tesseract OCR installed (`D:\Tesseract\tesseract.exe` by default path)
- Groq API key
- Required Python packages (see Installation)

## Installation 💻

1. Clone or download the OCR Forge CLI repository
2. Install required dependencies:
   ```
   pip install mss pillow pytesseract keyboard plyer requests groq rich
   ```
3. Set up your Groq API key as an environment variable:
   ```
   export GROQ_API_KEY="your_groq_api_key_here"  # Linux/macOS
   set GROQ_API_KEY=your_groq_api_key_here       # Windows CMD
   $env:GROQ_API_KEY="your_groq_api_key_here"    # Windows PowerShell
   ```
4. Ensure Tesseract OCR is installed. If needed, update the path in the script to match your installation:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"path\to\tesseract.exe"
   ```

## Usage 🛠️

### Starting the Application

Run the script from your terminal or command prompt:

```
python ocrforge.py
```

### Keyboard Shortcuts ⌨️

- **Ctrl + Print Screen** 📸: Activate the region selection tool for targeted screen capture
- **Esc** ❌: Exit the application

### Region Selection 🖱️

When you press **Ctrl + Print Screen**:
1. Your screen will dim and become semi-transparent
2. Click and drag to select the region you want to capture
3. Release the mouse button to confirm your selection
4. Press **Esc** to cancel the selection

### Follow-up Questions 💬

After text is captured and processed:
1. The cleaned text will be displayed in your terminal
2. You'll be prompted to ask follow-up questions about the captured text
3. Type your question at the prompt
4. Type `exit` to stop asking follow-up questions

### Viewing History 📜

To view your capture history:

```
python ocrforge.py --history
```

This will display the last 5 captures with their timestamps and cleaned text.

## How It Works ⚙️

1. **Screen Capture** 📸: 
   - Either full-screen or region-based using the MSS library
   - Image saved temporarily as PNG

2. **Text Extraction** 🔍:
   - Tesseract OCR extracts raw text from the image
   - Raw text is sent to Groq's LLM for processing

3. **LLM Processing** 🧠:
   - The Llama 3.3 70B Versatile model cleans and summarizes the text
   - Code blocks are automatically detected and highlighted

4. **User Interaction** 💬:
   - Follow-up questions are processed by the LLM with the context of the captured text
   - Responses are streamed in real-time

5. **History Management** 📚:
   - Each capture is logged with timestamp, raw text, and cleaned text
   - Log is stored in JSON format in `history_log.json`

## Configuration Options ⚙️

### Change Tesseract Path

Update the following line to match your Tesseract installation:

```python
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
```

### Change LLM Model

You can modify the Groq model used for processing by updating:

```python
model="llama-3.3-70b-versatile"
```

Available options include:
- `llama-3.3-70b-versatile`
- `llama3-8b-8192`

Adjust the temperature, token count, and other parameters as needed.

### Create your own history_log.json

To protect user privacy, no history_log.json file included in git repository, kindly create one before running the tool in the sam folder as the main.py py. I f you wish to store history somewhere else, specify it in config.py 

## Troubleshooting 🔧

### No Text Extracted ❌

If OCR fails to extract text:
- Try selecting a region with clearer text
- Ensure the text is visible and not obscured
- Check that Tesseract is properly installed and configured

### Groq API Errors ⚠️

If you encounter API errors:
- Verify your API key is correct and properly set
- Check your internet connection
- Ensure you have sufficient API credits

### Region Selection Issues 🖱️

If region selection doesn't work:
- Try restarting the application
- Ensure tkinter is properly installed
- Try using full-screen capture instead

## Files 📁

- `ocrforge.py`: Main application script
- `favicon.ico`: Icon file for notifications
- `history_log.json`: Log of captured text

## Contributing 👥

Contributions are welcome! Please feel free to submit a Pull Requestor create an issue.

## License 📄

MIT License

Copyright (c) 2025 Dewashish Lambore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments 🙏

- Created by Dewashish Lambore <a href="https://www.linkedin.com/in/dewashish-lambore-927048318/">Linkedin</a><a herf="https://github.com/DewashishCodes">GitHub</a>
- Uses Tesseract OCR for text extraction
- Uses Groq's LLM API for text processing

---
