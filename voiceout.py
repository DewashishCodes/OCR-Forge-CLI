# voiceout.py

import pyttsx3
import threading # Import threading module

# --- Global Settings ---
# Define these globally or pass them around
_speech_rate = 200
_male_voice_id = None # Will be set once at startup

def initialize_voice_settings(rate=200):
    """Initializes global voice settings (like finding male voice ID and rate).
       Needs to be called once at application startup."""
    global _speech_rate, _male_voice_id
    _speech_rate = rate
    try:
        # Use a temporary engine instance just to find the voice ID
        temp_engine = pyttsx3.init()
        voices = temp_engine.getProperty('voices')
        for voice in voices:
            if "male" in voice.name.lower():
                _male_voice_id = voice.id
                break
        # Crucially, stop the temporary engine instance
        temp_engine.stop()
        # print("Voice settings initialized.") # Optional debug
    except Exception as e:
        print(f"Warning: Could not initialize voice settings: {e}")
        _male_voice_id = None # Ensure it's None on failure

def _threaded_speak(text):
    """Initializes engine within the thread and speaks the text."""
    try:
        # Initialize engine *inside* the thread
        # This ensures thread-safety and avoids potential conflicts
        engine = pyttsx3.init()
        engine.setProperty('rate', _speech_rate)

        # Set the voice using the pre-discovered ID or default
        # Need to get voices again as the engine is new in this thread
        voices = engine.getProperty('voices')
        engine.setProperty('voice', _male_voice_id or voices[0].id)

        # print(f"Speaking in thread: {text[:50]}...") # Optional debug

        engine.say(text)
        engine.runAndWait() # This is the blocking call, but it's now in a separate thread
        engine.stop() # Clean up the engine instance in the thread

    except Exception as e:
        # Handle potential errors in the speech thread
        print(f"\nError in speech thread: {e}")

def speak(text):
    """Convert text to speech by running it in a separate thread."""
    if not text or not text.strip():
         # Avoid starting a thread for empty text
         return

    # Create a new thread targeting the _threaded_speak function
    speech_thread = threading.Thread(target=_threaded_speak, args=(text,))
    # Set the thread as a daemon. This allows the main program to exit even if this thread
    # hasn't finished speaking yet (though runAndWait should usually finish quickly).
    speech_thread.daemon = True
    # Start the thread
    speech_thread.start()
    # The speak function returns immediately, the main thread continues.

    # Note: You should *not* join the thread here unless you *want* the main
    # thread to wait for speech to finish (which is what caused the original problem).

# # Remove the old global engine initialization and voice setting code from here
# # It's replaced by initialize_voice_settings


# The speak function now just starts the thread
# def speak(text): # Old function - remove this
#     """Convert text to speech."""
#     engine.say(text)
#     engine.runAndWait()
#     return text