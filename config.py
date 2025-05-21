import os
import sys

# --- Configuration Constants ---
HISTORY_FILE = "./history_log.json"


# Set the path to Tesseract executable
# IMPORTANT: Change this to your Tesseract installation path
TESSERACT_CMD = r"D:\Tesseract\tesseract.exe" # Example path - CHANGE THIS

# Preferred Groq Model
GROQ_MODEL = "llama-3.3-70b-versatile" # Or "llama3-8b-8192"

HOTKEY="ctrl+print screen" # You can change according to your preference

# --- API Key Validation ---
def get_groq_api_key():
    """Retrieves and validates the Groq API key from environment variables."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not api_key.strip() or not api_key.startswith("gsk_"):
        print("❌ [ERROR] GROQ API key is missing or invalid.")
        print("➡️  Please set your GROQ_API_KEY environment variable.")
        sys.exit(1)
    return api_key

if __name__ == '__main__':
    # This block runs only if you execute config.py directly
    # Useful for just validating the setup
    print("Validating configuration...")
    try:
        key = get_groq_api_key()
        print("✅ GROQ_API_KEY found and seems valid (starts with 'gsk_').")
    except SystemExit:
        print("❌ GROQ_API_KEY not set or invalid.")

    print(f"History file set to: {HISTORY_FILE}")
    print(f"Tesseract command set to: {TESSERACT_CMD}")
    print(f"Default Groq model: {GROQ_MODEL}")