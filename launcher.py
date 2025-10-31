import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

# --------------------------
# CONFIG
# --------------------------
GITHUB_USER = "KSUhippiebus"
GITHUB_REPO = "cosmoTed"
BRANCH = "main"
EXCLUDE_FILE = "launcher.py"  # file to skip
# --------------------------

API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/git/trees/{BRANCH}?recursive=1"

def fetch_py_files():
    """Fetch all .py files from the repo, excluding EXCLUDE_FILE"""
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        data = resp.json()
        files = [item["path"]
                 for item in data.get("tree", [])
                 if item["type"] == "blob"
                 and item["path"].endswith(".py")
                 and EXCLUDE_FILE not in item["path"]]
        return files
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch file list:\n{e}")
        return []

def run_script(file_path):
    """Download and execute a Python file from GitHub"""
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{file_path}"
    try:
        r = requests.get(raw_url)
        r.raise_for_status()
        code = r.text
        # Optional: show the code in a window
        show_code_window(file_path, code)
        # Execute in separate namespace
        namespace = {}
        exec(code, namespace)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {file_path}:\n{e}")

def show_code_window(title, code):
    """Show the Python code in a scrollable window"""
    win = tk.Toplevel(root)
    win.title(f"{title} — Code")
    txt = scrolledtext.ScrolledText(win, wrap=tk.NONE, width=80, height=30)
    txt.insert(tk.END, code)
    txt.configure(state="disabled")
    txt.pack(fill=tk.BOTH, expand=True)

def on_button_click(path):
    # Run in a separate thread so UI remains responsive
    threading.Thread(target=run_script, args=(path,), daemon=True).start()

# --------------------------
# TKINTER GUI
# --------------------------
root = tk.Tk()
root.title(f"{GITHUB_REPO} Python Files")

main_frame = ttk.Frame(root, padding=(10,10))
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas_frame = canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Fetch and display buttons
files = fetch_py_files()
if not files:
    ttk.Label(scrollable_frame, text="No Python files found or fetch failed.").pack(pady=10)
else:
    for fpath in files:
        btn = ttk.Button(scrollable_frame, text=fpath,
                         command=lambda p=fpath: on_button_click(p))
        btn.pack(fill="x", pady=2)

root.mainloop()
