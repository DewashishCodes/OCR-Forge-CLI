import json
import os
from datetime import datetime
# Need the HISTORY_FILE path from main (or config)

def log_result(history_file, cleaned_text, raw_text=None):
    """Logs the capture result to a JSON file."""
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "raw_text": raw_text or "", # Log raw text as well
        "cleaned_text": cleaned_text
    }

    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                # Load existing history, handle empty or corrupted file
                history = json.load(f)
                if not isinstance(history, list): # Ensure it's a list
                     print(f"⚠️ History file {history_file} is not a list, starting new history.")
                     history = []
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle empty or corrupted file by starting a new history list
            print(f"⚠️ History file {history_file} empty or corrupted, starting new history.")
            history = []
    else:
        history = [] # Start new history if file doesn't exist

    history.append(entry)

    try:
        with open(history_file, "w", encoding="utf-8") as f:
            # Use ensure_ascii=False to correctly save non-ASCII characters
            json.dump(history, f, indent=2, ensure_ascii=False)
        # print(f"✅ Result logged to {history_file}") # Optional confirmation
    except Exception as e:
        print(f"❌ Error saving history to {history_file}: {e}")


def print_history(history_file, num_entries=5):
    """Displays the last few entries from the history log."""
    if not os.path.exists(history_file):
        print("📭 No history file found.")
        return
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
            if not isinstance(history, list):
                 print(f"⚠️ History file {history_file} is corrupted (not a list).")
                 return
    except json.JSONDecodeError:
        print(f"⚠️ History file {history_file} is empty or corrupted.")
        return
    except Exception as e:
         print(f"❌ Error reading history file {history_file}: {e}")
         return


    if not history:
        print("📭 History is empty.")
        return

    print(f"\n--- Last {min(num_entries, len(history))} History Entries ---")
    # Show the last num_entries
    for idx, entry in enumerate(history[-num_entries:], 1):
        print(f"\nEntry {idx}:")
        print(f"  🕒 {entry.get('timestamp', 'N/A')}")
        print("  📜 Cleaned Text:")
        print("  ----------------------------")
        # Use .get() for safety in case schema changes
        print(entry.get("cleaned_text", "[Missing Cleaned Text]"))
        print("  ----------------------------")
        # Optionally print raw text too
        # print("  📄 Raw Text:")
        # print("  ----------------------------")
        # print(entry.get("raw_text", "[Missing Raw Text]"))
        # print("  ----------------------------")
    print("\n--- End of History ---")