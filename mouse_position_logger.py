
import pyautogui
import keyboard
import time

saved_positions = []

print("🔍 Move the mouse. Press [Enter] to save the position. Exit with [Ctrl+C].")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Position: x={x}, y={y}", end="\r")
        if keyboard.is_pressed('enter'):
            saved_positions.append((x, y))
            print(f"\n✅ Saved: x={x}, y={y}")
            time.sleep(0.3)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n\n📝 Saved positions:")
    for i, (x, y) in enumerate(saved_positions, 1):
        print(f"{i}. x={x}, y={y}")
    print("\nDone.")
