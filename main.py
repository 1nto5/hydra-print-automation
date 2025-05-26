# FastAPI server for automating print operations in HYDRA system
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from threading import Thread
from multiprocessing import Process
import time
import tkinter as tk
from pywinauto import Application, Desktop
import pyautogui
import logging

# Configure logging to both file and console
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI()

# Global variables for window management
focused_chrome_window = {"title": None}
status_process = None

# Request model for automation endpoint
class AutomationRequest(BaseModel):
    identifier: str
    quantity: str
    workplace_position: int = Field(default=1, ge=1, le=4, description="Workplace position (1-4)")

def remember_active_window_title():
    """Store the title of the currently active Chrome window for later restoration"""
    global focused_chrome_window
    try:
        windows = Desktop(backend="win32").windows()
        for w in windows:
            if "Chrome" in w.window_text():
                focused_chrome_window["title"] = w.window_text()
                return
    except Exception as e:
        logger.error(f"Error remembering Chrome window: {e}")

def restore_chrome():
    """Restore the previously active Chrome window"""
    global focused_chrome_window
    try:
        if focused_chrome_window["title"]:
            app = Application(backend="win32").connect(title=focused_chrome_window["title"])
            win = app.top_window()
            if win.is_minimized():
                win.restore()
            win.set_focus()
    except Exception as e:
        logger.error(f"Error restoring Chrome window: {e}")

def status_window_fn():
    """Create and display a status window showing automation progress"""
    win = tk.Tk()
    screen_width = win.winfo_screenwidth()
    win.geometry(f"{screen_width}x60+0+0")
    win.attributes("-topmost", True)
    win.overrideredirect(True)
    win.configure(bg="red")
    win.resizable(False, False)

    label = tk.Label(
        win,
        text="HYDRA Print Automation in progress... Please wait",
        fg="white",
        bg="red",
        font=("Segoe UI", 18, "bold")
    )
    label.pack(expand=True)
    win.mainloop()

def show_status_window():
    """Start the status window in a separate process"""
    global status_process
    status_process = Process(target=status_window_fn)
    status_process.start()

def close_status_window():
    """Terminate the status window process"""
    global status_process
    if status_process is not None:
        status_process.terminate()
        status_process.join()
        status_process = None

def automation_task(identifier: str, quantity: str, workplace_position: int = 1):
    """
    Main automation sequence for print operations
    
    Args:
        identifier: The identifier to be entered in the system
        quantity: The quantity to be entered in the system
        workplace_position: Position number (1-4) for workplace selection
    """
    show_status_window()
    remember_active_window_title()

    try:
        # Find and focus the window
        matches = Desktop(backend="win32").windows(title_re=".*AIP.*")
        if not matches:
            logger.error("No AIP window found")
            return

        win = matches[0]
        if win.is_minimized():
            win.restore()
        win.set_focus()
        time.sleep(0.5)

        # Initial click to ensure operation window focus
        pyautogui.click(x=1254, y=623) 
        time.sleep(1)

        # Select workplace position with vertical offset
        workplace_y = 77 + (workplace_position - 1) * 73
        pyautogui.click(x=150, y=workplace_y) 
        time.sleep(1)

        # Click operation
        pyautogui.click(x=466, y=407) 
        time.sleep(1)

        # Click output batch
        pyautogui.click(x=129, y=652) 
        time.sleep(1)

        # Focus and enter quantity
        pyautogui.click(x=813, y=248) 
        time.sleep(0.5)
        pyautogui.write(quantity)
        time.sleep(0.5)
        
        # Focus and enter identifier
        pyautogui.click(x=293, y=632) 
        time.sleep(0.5)
        pyautogui.write(identifier)
        time.sleep(0.5)

        # Click print button
        pyautogui.click(x=1191, y=711) 
        time.sleep(1)

    except Exception as e:
        logger.error(f"Automation error: {e}")
        raise

    # Restore previous window state
    time.sleep(2.5)
    restore_chrome()
    time.sleep(0.5)
    close_status_window()

@app.post("/run-aip-print-automation")
async def run_automation(request: Request, body: AutomationRequest):
    """
    API endpoint to trigger the automation sequence
    
    Args:
        request: FastAPI request object
        body: AutomationRequest containing identifier and optional workplace position
    
    Returns:
        dict: Status of the automation request
    """
    thread = Thread(target=automation_task, args=(body.identifier, body.quantity, body.workplace_position))
    thread.start()
    return {"status": "started"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)