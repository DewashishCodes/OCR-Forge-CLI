import sys
import os
import keyboard # For hotkey binding
from groq import Groq # To initialize the client

# Import the modules we created
import config
import capture
import ocr
import llm
import history
import display

# --- Initial Setup ---

# Print the ASCII art banner
print("\n\n")
print(r"  ____  ________  ____                    _______   ____")  
print(r" / __ \/ ___/ _ \/ __/__  _______ ____   / ___/ /  /  _/")   
print(r"/ /_/ / /__/ , _/ _// _ \/ __/ _ `/ -_) / /__/ /___/ /")     
print(r"\____/\___/_/|_/_/  \___/_/  \_, /\__/  \___/____/___/")    
print(r"                            /___/                      created by Dewashish Lambore   ")

# Validate API Key and initialize Groq client
try:
    groq_api_key = config.get_groq_api_key()
    groq_client = Groq(api_key=groq_api_key)
    print("✅ Groq client initialized.")
except SystemExit: # get_groq_api_key exits on failure
    sys.exit(1)
except Exception as e:
     print(f"❌ Failed to initialize Groq client: {e}")
     sys.exit(1)

# Set Tesseract command path
ocr.set_tesseract_cmd(config.TESSERACT_CMD)
# Optional: Add a check here to see if Tesseract executable exists/works

# Check for history command-line argument
if "--history" in sys.argv:
    history.print_history(config.HISTORY_FILE)
    sys.exit(0)

# --- Main Capture & Process Flow ---

def process_captured_image(image_path):
    """Handles OCR, LLM cleanup, display, and history logging for a given image file."""

    if not image_path or not os.path.exists(image_path):
         print("❌ No valid image file provided to process.")
         display.send_notification(
            title='Processing Failed',
            message='Image file missing.',
            app_name="OCRforge CLI",
            
        )
         # Return an error message as context
         return "[Image Processing Failed]"

    print("🔍 Extracting text...")
    raw_text = ocr.extract_text_from_image(image_path)

    # Clean up the temporary screenshot file after OCR
    capture.cleanup_temp_image(image_path)

    # Check if OCR failed or returned no text
    if not raw_text or raw_text.strip().startswith("["): # Starts with '[' typically indicates our internal error messages
         print("⚠️ No text extracted or error occurred during OCR.")
         # Log the error message/lack of text as the "cleaned" result
         # Use the raw_text variable which contains the specific error message if any
         logged_cleaned_text = raw_text.strip() if raw_text and raw_text.strip() else "[No text extracted]"
         history.log_result(config.HISTORY_FILE, logged_cleaned_text, raw_text)
         display.send_notification(
            title='No Text Found',
            message='Could not extract text from the image.',
            timeout=5,
            app_name="OCRforge CLI"
           
         )
         return logged_cleaned_text # Return error/empty message as context


    # Proceed to LLM cleanup if OCR was successful
    cleaned_text = llm.clean_text_with_llm(groq_client, raw_text, config.GROQ_MODEL)

    display.send_notification(
        title='Text Ready',
        message='Cleaned and summarized text available!',
        timeout=5,
        app_name="OCRforge CLI"
        
    )

    print("\n✅ Final Relevant Text:\n----------------------")
    display.display_output(cleaned_text) # Use the improved display function
    print("----------------------\n")

    # Log the results
    history.log_result(config.HISTORY_FILE, cleaned_text, raw_text)

    return cleaned_text # Return cleaned text as context for follow-up


# --- Hotkey Triggered Functions ---

# Original logic used special_process for region capture.
# We'll rename and use the new modular functions.

def trigger_region_capture():
    """Initiates the screen region selection and processing."""
    display.send_notification(
        title='Screen Capture Initiated',
        message='Select a region to capture...',
        timeout=3, # Short timeout as window will appear
        app_name="OCRforge CLI"
       
    )
    print("\n🖱️ Draw a rectangle on the screen to select the capture region.")
    print(" Press Esc to cancel.")

    # This call opens the Tkinter window and blocks until selection is done
    selected_box = capture.capture_region()

    if not selected_box:
        print("🛑 Region selection cancelled or failed.")
        current_context = "[Region Selection Cancelled]" # Update context state
        history.log_result(config.HISTORY_FILE, current_context, "[Region Selection Cancelled]")
        display.send_notification(
            title='Capture Cancelled',
            message='Screen region selection cancelled.',
            timeout=3,
            app_name="OCRforge CLI"
            
        )
        # No further processing if selection failed/cancelled
        return # Exit the function early

    # Proceed with capture using the selected region coordinates
    display.send_notification(
        title='Region Selected',
        message='Capturing selected area and extracting text...',
        timeout=5,
        app_name="OCRforge CLI"
        
    )

    print("\n📸 Capturing selected region...")
    image_path = capture.capture_image_from_box(selected_box)

    if image_path:
        # Process the captured image (OCR, LLM, display, log)
        current_context = process_captured_image(image_path)
        # The process_captured_image function already handles cleaning up the image file

        # Now, allow follow-up questions using the generated context
        llm.follow_up_prompt(groq_client, current_context, config.GROQ_MODEL)
    else:
        print("❌ Region screen capture failed.")
        current_context = "[Region Capture Failed]" # Update context state
        history.log_result(config.HISTORY_FILE, current_context, "[Region Capture Failed]")
        # No follow-up prompt if capture failed


# Optional: Function to trigger full screen capture, if you want to bind it
def trigger_full_screen_capture():
    """Initiates full screen capture and processing."""
    display.send_notification(
        title='Screen Capture Started',
        message='Capturing full screen...',
        timeout=5,
        app_name="OCRforge CLI",
        
    )
    print("\n📸 Capturing full screen...")
    image_path = capture.capture_full_screen()

    if image_path:
        current_context = process_captured_image(image_path)
         # The process_captured_image function already handles cleaning up the image file
        llm.follow_up_prompt(groq_client, current_context, config.GROQ_MODEL)
    else:
        print("❌ Full screen capture failed.")
        current_context = "[Full Screen Capture Failed]"
        history.log_result(config.HISTORY_FILE, current_context, "[Full Screen Capture Failed]")
        # No follow-up prompt if capture failed


# --- Main Execution Loop ---
print("\n🚀 OCR Assistant with Groq is running.")
print("🎯 Select a region with Ctrl + PrtScn to capture text.")
# print("Capture full screen with Shift + PrtScn (Optional - if enabled).") # Uncomment if you add the binding
print("❌ Press Esc to quit.")
print(f"📖 View history with: python {os.path.basename(__file__)} --history")


# Bind the shortcut (Ctrl + Print Screen) to trigger region capture
keyboard.add_hotkey(config.HOTKEY, trigger_region_capture)

# Bind another shortcut for full screen if desired (e.g., Shift + Print Screen)
# keyboard.add_hotkey('shift+print screen', trigger_full_screen_capture)


# Keep the script running, waiting for hotkey presses, until 'Esc' is pressed
try:
    keyboard.wait('esc')
except Exception as e:
    # This exception is expected when the main thread is told to exit
    # while keyboard.wait is active. We can ignore it or print a specific message.
    # Printing a specific message might be less alarming than the traceback.
    # print(f"\nAn expected interruption occurred while waiting for Esc: {e}")
    pass # Simply ignore the interruption exception

print("\nShutting down OCRforge.")
sys.exit(0)