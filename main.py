import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from threading import Thread
from multiprocessing import Process
import time
import tkinter as tk
from pywinauto import Application, Desktop
import pyautogui
import subprocess
import os
from typing import Dict

app = FastAPI()

# Get API token from environment variable
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError(
        "API_TOKEN environment variable is not set. "
        "Please set it using: export API_TOKEN=your_token_here"
    )

focused_chrome_window = {"title": None}
status_process = None

class AutomationRequest(BaseModel):
    identifier: str
    variant_position: int = Field(default=1, ge=1, le=4, description="Variant position (1-4)")
    machine_position: int = Field(default=1, ge=1, le=4, description="Machine position (1-4)")

class UpdateResponse(BaseModel):
    status: str
    message: str
    details: Dict = {}

def remember_active_window_title():
    global focused_chrome_window
    try:
        windows = Desktop(backend="win32").windows()
        for w in windows:
            if "Chrome" in w.window_text():
                focused_chrome_window["title"] = w.window_text()
                return
    except Exception as e:
        print("Error remembering Chrome window:", e)

def restore_chrome():
    global focused_chrome_window
    try:
        if focused_chrome_window["title"]:
            app = Application(backend="win32").connect(title=focused_chrome_window["title"])
            win = app.top_window()
            if win.is_minimized():
                win.restore()
            win.set_focus()
    except Exception as e:
        print("Error restoring Chrome window:", e)

def status_window_fn():
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
    global status_process
    status_process = Process(target=status_window_fn)
    status_process.start()

def close_status_window():
    global status_process
    if status_process is not None:
        status_process.terminate()
        status_process.join()
        status_process = None

def automation_task(identifier: str, variant_position: int = 1, machine_position: int = 1):
    show_status_window()
    
    remember_active_window_title()

    try:
        matches = Desktop(backend="win32").windows(title_re=".*AIP.*")
        if not matches:
            return

        win = matches[0]
        if win.is_minimized():
            win.restore()
        win.set_focus()
        time.sleep(0.5)

        # Predefined Y coordinates for variant selection
        variant_positions = {
            1: 639,  # First variant
            2: 669,  # Second variant
            3: 699,  # Third variant
            4: 729   # Fourth variant
        }
        variant_y = variant_positions.get(variant_position, 639)
        pyautogui.click(x=1266, y=variant_y)
        time.sleep(1)

        # Machine selection with 30px vertical offset between positions
        machine_y = 419 + (machine_position - 1) * 30
        pyautogui.click(x=469, y=machine_y)
        time.sleep(1)

        # Navigation and identifier input sequence
        pyautogui.click(x=114, y=654)
        time.sleep(1)

        pyautogui.click(x=286, y=636)
        time.sleep(0.5)
        pyautogui.write(identifier)
        time.sleep(0.5)

        pyautogui.click(x=1226, y=708)
        time.sleep(1)

    except Exception as e:
        print("Automation error:", e)

    time.sleep(0.5)
    restore_chrome()
    time.sleep(0.5)
    close_status_window()

@app.post("/run-automation")
async def run_automation(request: Request, body: AutomationRequest):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    thread = Thread(target=automation_task, args=(body.identifier, body.variant_position, body.machine_position))
    thread.start()
    return {"status": "started"}

@app.post("/update")
async def update_from_github(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        # Fetch latest changes
        subprocess.run(["git", "fetch", "origin"], check=True)
        
        # Get current branch
        current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        
        # Get local and remote commit hashes
        local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        remote_commit = subprocess.check_output(["git", "rev-parse", f"origin/{current_branch}"]).decode().strip()
        
        if local_commit == remote_commit:
            return UpdateResponse(
                status="success",
                message="Already up to date",
                details={"local_commit": local_commit}
            )
        
        # Pull latest changes
        subprocess.run(["git", "pull", "origin", current_branch], check=True)
        
        # Install/update dependencies if requirements.txt changed
        if subprocess.run(["git", "diff", "--name-only", local_commit, "HEAD"], 
                        capture_output=True, text=True).stdout.strip().split("\n"):
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        
        return UpdateResponse(
            status="success",
            message="Update completed successfully",
            details={
                "previous_commit": local_commit,
                "new_commit": remote_commit
            }
        )
        
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during update: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)