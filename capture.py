import mss
from PIL import Image
import tkinter as tk
from tkinter import Canvas
import os
# We will need the APP_ICON and send_notification from other modules,
# but for modularity, this file focuses only on capture logic.
# The main orchestrator (main.py) will handle notifications and paths.

class ScreenRegionSelector:
    """A Tkinter overlay to select a screen region."""
    def __init__(self, master):
        self.master = master
        # Set window properties for overlay
        self.master.attributes('-fullscreen', True)
        self.master.attributes('-alpha', 0.3) # Semi-transparent overlay
        self.master.attributes('-topmost', True)
        self.master.overrideredirect(True) # No window borders/title bar

        # Canvas to draw the selection rectangle
        self.canvas = Canvas(master, cursor="crosshair", bg='gray') # Background for alpha effect
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.captured_box = None # Stores the final {left, top, width, height} dict for mss

        # Bind mouse events for drawing
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Bind Escape key to cancel
        self.master.bind("<Escape>", self.on_escape)

    def on_button_press(self, event):
        """Records the starting point of the drag."""
        self.start_x = event.x
        self.start_y = event.y
        # Delete previous rectangle if any
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = None
        self.captured_box = None # Reset captured box

    def on_motion(self, event):
        """Updates the selection rectangle as the mouse is dragged."""
        if self.start_x is not None and self.start_y is not None:
            if self.rect_id:
                self.canvas.delete(self.rect_id)
            # Draw the rectangle
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y
            # Draw with transparent fill and a border
            self.rect_id = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                        outline='red', width=2, fill='', tags='selection_rect')

    def on_button_release(self, event):
        """Records the end point and finalizes the selection."""
        if self.start_x is not None and self.start_y is not None:
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y

            # Ensure x1,y1 is top-left and x2,y2 is bottom-right
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)

            width = right - left
            height = bottom - top

            # Store the coordinates as a dictionary for mss
            # Only store if a valid region was selected (more than a minimal size)
            if width > 5 and height > 5: # Minimum size threshold
                 # Tkinter coordinates in fullscreen overrideredirect map directly to screen coords
                 self.captured_box = {'top': top, 'left': left, 'width': width, 'height': height}
                 print(f"✅ Region selected: {self.captured_box}")
            else:
                 print("⚠️ Selection region too small or no region selected.")
                 self.captured_box = None # Explicitly set to None if too small or single click

            # Close the selection window
            self.master.destroy()

    def on_escape(self, event):
        """Cancels the selection and closes the window."""
        print("↩️ Selection cancelled.")
        self.captured_box = None # Explicitly None on cancel
        self.master.destroy()

def capture_full_screen():
    """Captures the primary screen (monitor 1)."""
    image_path = "screenshot_full.png" # Temporary file name
    try:
        with mss.mss() as sct:
            # Capture primary monitor (index 1 in mss is usually the primary)
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            img.save(image_path)
            print(f"Full screenshot saved to {image_path}")
            return image_path
    except mss.exception.ScreenShotError as e:
        print(f"❌ Error capturing full screen with mss: {e}")
        return None
    except Exception as e:
         print(f"❌ Unexpected error during full screen capture: {e}")
         return None

def capture_region():
    """Opens the screen region selector UI and returns the selected box."""
    root = tk.Tk()
    selector = ScreenRegionSelector(root)
    root.mainloop() # This blocks until the selection window is closed
    return selector.captured_box # Returns the {'top', 'left', 'width', 'height'} dict or None

def capture_image_from_box(box):
    """Captures an image using the given mss box dictionary."""
    if not box:
        print("Error: No capture box provided.")
        return None
    image_path = "screenshot_region.png" # Temporary file name
    try:
        with mss.mss() as sct:
             # Ensure coordinates are valid if needed, mss is usually robust
             sct_img = sct.grab(box)
             img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
             img.save(image_path)
             print(f"Region screenshot saved to {image_path}")
             return image_path
    except mss.exception.ScreenShotError as e:
        print(f"❌ Error capturing region with mss: {e}")
        return None
    except Exception as e:
         print(f"❌ Unexpected error during region screen capture: {e}")
         return None

# Helper to clean up temp files - main.py will call this
def cleanup_temp_image(image_path):
    """Deletes a temporary image file if it exists."""
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
            print(f"Cleaned up {image_path}")
        except OSError as e:
            print(f"⚠️ Error cleaning up screenshot file {image_path}: {e}")