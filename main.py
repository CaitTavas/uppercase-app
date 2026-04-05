import tkinter as tk
from tkinter import font as tkfont
import pyperclip
import keyboard
import pyautogui
import time
import sys

# ── Config ───────────────────────────────────────────────────────────────────
HOTKEY = "ctrl+shift+u"

# ── State ────────────────────────────────────────────────────────────────────
active = False
hotkey_registered = False


def uppercase_selection():
    try:
        original_clipboard = pyperclip.paste()
    except Exception:
        original_clipboard = ""

    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.12)

    try:
        selected = pyperclip.paste()
    except Exception:
        selected = ""

    if selected and selected != original_clipboard:
        pyperclip.copy(selected.upper())
        time.sleep(0.05)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.05)
        pyperclip.copy(original_clipboard)
        preview = selected[:28] + "…" if len(selected) > 28 else selected
        flash_status(f'✔  "{preview}"')
    else:
        flash_status("⚠  Nothing selected")


def flash_status(msg):
    status_var.set(msg)
    root.after(2500, lambda: status_var.set("Listening…" if active else "Paused"))


def toggle():
    global active, hotkey_registered
    active = not active

    if active:
        if not hotkey_registered:
            keyboard.add_hotkey(HOTKEY, uppercase_selection)
            hotkey_registered = True
        btn.config(text="⏹  Stop", bg="#e05252", activebackground="#c94444")
        indicator.config(bg="#4caf50")
        status_var.set("Listening…")
        log(f"Started — press {HOTKEY.upper()} over selected text")
    else:
        if hotkey_registered:
            keyboard.remove_hotkey(HOTKEY)
            hotkey_registered = False
        btn.config(text="▶  Start", bg="#4caf50", activebackground="#3d9140")
        indicator.config(bg="#e05252")
        status_var.set("Paused")
        log("Stopped")


def log(msg):
    log_box.config(state="normal")
    log_box.insert("end", f"• {msg}\n")
    log_box.see("end")
    log_box.config(state="disabled")


def on_close():
    global hotkey_registered
    if hotkey_registered:
        try:
            keyboard.remove_hotkey(HOTKEY)
        except Exception:
            pass
    root.destroy()
    sys.exit(0)


root = tk.Tk()
root.title("UPPERCASE Tool")
root.geometry("600x360")
root.minsize(400, 220)
root.resizable(False, False)
root.configure(bg="#1e1e2e")
root.protocol("WM_DELETE_WINDOW", on_close)
root.attributes("-topmost", True)

title_font  = tkfont.Font(family="Courier New", size=15, weight="bold")
mono_font   = tkfont.Font(family="Courier New", size=9)
status_font = tkfont.Font(family="Courier New", size=10)

header_frame = tk.Frame(root, bg="#1e1e2e")
header_frame.pack(pady=(18, 4))

indicator = tk.Label(header_frame, text="  ", bg="#e05252", width=2)
indicator.pack(side="left", padx=(0, 8))

tk.Label(header_frame, text="UPPERCASE TOOL",
         font=title_font, bg="#1e1e2e", fg="#cdd6f4").pack(side="left")

tk.Label(root, text=f"Hotkey: {HOTKEY.upper()}",
         font=mono_font, bg="#1e1e2e", fg="#6c7086").pack()

btn = tk.Button(root, text="▶  Start",
                font=tkfont.Font(family="Courier New", size=12, weight="bold"),
                bg="#4caf50", activebackground="#3d9140",
                fg="white", activeforeground="white",
                relief="flat", cursor="hand2",
                width=16, height=1, command=toggle)
btn.pack(pady=14)

status_var = tk.StringVar(value="Paused")
tk.Label(root, textvariable=status_var,
         font=status_font, bg="#1e1e2e", fg="#a6e3a1").pack()

log_frame = tk.Frame(root, bg="#1e1e2e")
log_frame.pack(fill="both", expand=True, padx=16, pady=(10, 16))

log_box = tk.Text(log_frame, height=6, font=mono_font,
                  bg="#181825", fg="#cdd6f4", relief="flat", bd=0,
                  state="disabled", wrap="word", cursor="arrow")
log_box.pack(fill="both", expand=True)

log(f"Ready — press Start, then use {HOTKEY.upper()} to uppercase selected text")

root.mainloop()