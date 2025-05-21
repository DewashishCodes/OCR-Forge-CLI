# OCR Forge CLI Setup Guide

This guide will walk you through the complete setup process for OCR Forge CLI, including detailed instructions for installing all dependencies and configuring the application.

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.6 or higher
- **Disk Space**: At least 200MB for dependencies and Tesseract OCR
- **RAM**: Minimum 4GB recommended
- **Internet Connection**: Required for LLM API calls

## Installation Steps

### 1. Install Python (if not already installed)

Visit [python.org](https://www.python.org/downloads/) and download the latest version for your operating system.

During installation on Windows:
- ✅ Check "Add Python to PATH"
- ✅ Check "Install pip"

Verify installation by opening a terminal/command prompt and typing:
```bash
python --version
pip --version
```

### 2. Install Tesseract OCR

#### Windows:
1. Download the installer from [GitHub UB Mannheim Tesseract repository](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and note the installation path (default is `C:\Program Files\Tesseract-OCR`)
3. You may need to add Tesseract to your PATH:
   - Right-click on 'This PC' > Properties > Advanced system settings > Environment Variables
   - Edit the Path variable and add the Tesseract installation directory

#### macOS:
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install tesseract-ocr
```

Verify installation:
```bash
tesseract --version
```

### 3. Set Up OCR Forge CLI

1. Download the OCR Forge CLI script:
   ```bash
   # Create a directory for the application
   mkdir ocrforge
   cd ocrforge
   
   # Download the script (replace with actual download URL if available)
   curl -o curseforge.py https://raw.githubusercontent.com/username/ocrforge/main/curseforge.py
   # OR copy the script manually to this directory
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install mss pillow pytesseract keyboard plyer requests groq rich
   ```

### 4. Configure Tesseract Path

Open `curseforge.py` in a text editor and update the Tesseract path to match your installation:

```python
# Find this line and update it with your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"

# Examples for different operating systems:
# Windows: r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# macOS/Linux: r"/usr/bin/tesseract"
# Use 'which tesseract' on macOS/Linux to find the path
```

### 5. Set Up Groq API

1. Sign up for a Groq account at [groq.com](https://groq.com)
2. Generate an API key from your Groq dashboard
3. Set the API key as an environment variable:

   #### Windows (Command Prompt):
   ```batch
   set GROQ_API_KEY=gsk_your_api_key_here
   ```
   
   #### Windows (PowerShell):
   ```powershell
   $env:GROQ_API_KEY="gsk_your_api_key_here"
   ```
   
   #### macOS/Linux:
   ```bash
   export GROQ_API_KEY="gsk_your_api_key_here"
   ```
   
   To make this permanent:
   - Windows: Add to System Environment Variables
   - macOS/Linux: Add to `~/.bashrc` or `~/.zshrc`

### 6. Create an Icon File (Optional)

The application looks for `favicon.ico` in the current directory for notifications. You can:
- Create or download an icon file named `favicon.ico`
- Place it in the same directory as `curseforge.py`
- Or update the `APP_ICON` variable in the script to point to your icon file

### 7. Test the Installation

Run the application:
```bash
python curseforge.py
```

You should see the OCR Forge CLI banner and instructions.

## Updating OCR Forge CLI

To update the application in the future:
1. Download the latest version of `curseforge.py`
2. Replace your existing file
3. If new dependencies are required, run:
   ```bash
   pip install -r requirements.txt  # If a requirements file is provided
   # OR
   pip install [new_package_name]   # For specific new packages
   ```

## Common Issues and Solutions

### Permission Issues

**Problem**: Unable to run keyboard hooks due to permission issues.  
**Solution**: Run the script as administrator (Windows) or with sudo (macOS/Linux).

### Tesseract Not Found

**Problem**: Error message about Tesseract not being found.  
**Solution**: Double-check the path in the script and ensure Tesseract is properly installed.

### API Key Issues

**Problem**: "GROQ API key is missing or invalid" error.  
**Solution**: Verify your API key is correctly set as an environment variable and starts with "gsk_".

### Screen Capture Issues

**Problem**: Unable to capture screen regions.  
**Solution**: Ensure you have the necessary permissions for screen recording on your OS.

## Additional Configuration Options

### Customizing LLM Parameters

You can modify these parameters in the script for different results:

```python
# Find these parameters in the clean_text_with_llm function
chat_completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Model choice
    messages=[...],
    temperature=0.3,  # Lower = more deterministic, higher = more creative
    max_tokens=300,   # Maximum response length
    top_p=1,          # Controls diversity
    stream=True       # Enable streaming responses
)
```

### Changing History File Location

By default, history is stored in `./history_log.json`. To change this:

```python
# Find this line near the top of the script
HISTORY_FILE = "./history_log.json"

# Change to your preferred location, such as:
HISTORY_FILE = "/path/to/your/preferred/location/history_log.json"
```

## Uninstallation

To remove OCR Forge CLI:

1. Delete the application directory containing `curseforge.py`
2. Optionally uninstall Python packages:
   ```bash
   pip uninstall mss pillow pytesseract keyboard plyer requests groq rich
   ```
3. Tesseract OCR can be uninstalled through your system's standard uninstallation process