import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from threading import Thread
from multiprocessing import Process
import time
import tkinter as tk
from pywinauto import Application, Desktop
import pyautogui

app = FastAPI()
API_TOKEN = "ad126ea0-a92b-4ce5-9c77-e8d9024d9867"

focused_chrome_window = {"title": None}
status_process = None

class AutomationRequest(BaseModel):
    identifier: str

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

def automation_task(identifier: str):
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

        pyautogui.click(x=1266, y=639)
        time.sleep(1)

        pyautogui.click(x=469, y=419)
        time.sleep(1)

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

    thread = Thread(target=automation_task, args=(body.identifier,))
    thread.start()
    return {"status": "started"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)