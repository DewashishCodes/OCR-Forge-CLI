from rich.console import Console
from rich.syntax import Syntax
import re
from plyer import notification
import os
# Need APP_ICON path from config (implicitly used via app_icon_path parameter)

console = Console()

def display_output(text):
    """Displays text using rich, attempting to highlight markdown code blocks."""
    if not text:
        console.print("[italic grey]No text to display.[/italic grey]")
        return

    # Pattern to find fenced code blocks (```lang\ncode\n```)
    # Includes the delimiters and potentially language hint
    # Use non-greedy match `.*?` and DOTALL flag
    code_block_pattern = re.compile(r"(```(?:\w+)?\n.*?```)", re.DOTALL)

    last_end = 0
    for match in code_block_pattern.finditer(text):
        # Print text before this match
        if match.start() > last_end:
            console.print(text[last_end:match.start()].strip())

        # Process the code block
        block_text = match.group(1)
        lines = block_text.strip().split('\n')

        # Check if the block has at least start and end delimiters
        if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
            # Extract language hint from the first line (e.g., ```python)
            first_line = lines[0].strip()
            lang_match = re.match(r"```(\w+)?", first_line)
            # Use the matched language or default to None for auto-detection
            lang = lang_match.group(1) if lang_match else None

            # Extract code lines (all lines between the delimiters)
            code = "\n".join(lines[1:-1])

            # Display highlighted syntax
            try:
                # Use 'text' as a fallback language if None or detection fails
                syntax = Syntax(code, lang if lang else "text", theme="monokai", line_numbers=False)
                console.print(syntax)
            except Exception as e:
                # Fallback if syntax highlighting fails (e.g., invalid lang, weird code)
                console.print(f"[yellow]⚠️ Could not highlight code block (lang='{lang}'): {e}[/yellow]")
                console.print(block_text.strip()) # Print raw block instead


        else:
            # Handle malformed block (e.g., just ``` or ```lang without code, or missing end ```)
            # Print the raw block as text
            console.print(block_text.strip())


        last_end = match.end()

    # Print any remaining text after the last match
    if last_end < len(text):
        console.print(text[last_end:].strip())

# --- CORRECTED FUNCTION ---
def send_notification(title, message, app_name, timeout=5):
    """Sends a desktop notification."""
    # Check if icon exists before using (plyer might have issues otherwise)
    # Use a default icon path if the provided one doesn't exist
  
    # Note: APP_ICON is defined in config.py, main.py needs to pass it

    try:
        notification.notify(
            title=title,
            message=message,
            timeout=timeout, # <-- UNCOMMENTED and using the passed 'timeout' parameter
            app_name=app_name,
            
        )
    except Exception as e:
        print(f"⚠️ Could not send notification: {e}")